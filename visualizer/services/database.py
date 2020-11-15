""" A services to populate the journey in the database """

import datetime as dt
# import requests
import asyncio
import aiohttp

from aiohttp import ClientSession

from flask import current_app
from marshmallow.exceptions import ValidationError
from json import JSONDecodeError

from .. import db
from ..models.journey import Journey
from ..models.vendor import Vendor
from ..models.mapquest import response_body_schema
from ..models import data_refresh_db_input_schema
from .mock.tours import get_tours_data


def populate_database(refresh=False):
    """
    Function to populate the database with the data from csv file.
    Only run this once, otherwise you will have duplicate data.
    """
    print('Begin populating')

    journey_obj_list = list()

    if refresh is True:
        print('Refresh is set to true, delete all existing data')
        db.engine.execute("ALTER SEQUENCE journey_id_seq RESTART WITH 1")
        db.engine.execute("ALTER SEQUENCE vendor_id_seq RESTART WITH 1")

        journey_deleted = Journey.query.delete()
        if journey_deleted > 0:
            # db.session.delete(journey_deleted)
            print(f'{journey_deleted} journey(s) in the database are deleted')

        vendor_deleted = Vendor.query.delete()
        if vendor_deleted > 0:
            # db.session.delete(vendor_deleted)
            print(f'{vendor_deleted} vendor(s) in the database are deleted')
        db.session.commit()

        journey_data_list = get_tours_data()
        vendor_count = 0
        for journey_data in journey_data_list:
            if vendor_count < int(journey_data['\ufeffVendorID']):
                vendor_count = vendor_count + 1
                new_vendor = Vendor(name=f'Vendor{vendor_count}')
                new_vendor.save()

            new_journey = Journey(
                vendor_id=int(journey_data['\ufeffVendorID']),
                passenger_count=int(journey_data['passenger_count']),
                pickup_longitude=float(journey_data['pickup_longitude']),
                pickup_latitude=float(journey_data['pickup_latitude']),
                dropoff_longitude=float(journey_data['dropoff_longitude']),
                dropoff_latitude=float(journey_data['dropoff_latitude']),
                pickup_time=convert_to_datetime(
                    journey_data['pickup_date'], journey_data['pickup_time']),
                dropoff_time=convert_to_datetime(
                    journey_data['dropoff_date'], journey_data['dropoff_time']),
                total_fare_amount=float(journey_data['total_amount'])
            )
            journey_obj_list.append(new_journey)

    else:
        journey_obj_list = Journey.get_all()

    mapquest_limit = current_app.config['MAPQUEST_LIMIT_REQUEST']
    if mapquest_limit is not None:
        print(f'Assigining distance to {len(journey_obj_list)} journeys with max of {mapquest_limit} per request')
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(assign_distance(journey_obj_list, limit=mapquest_limit))
    else:
        print(f'Assigining distance to {len(journey_obj_list)} journeys without limit per request')
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(assign_distance(journey_obj_list))

    print('finish populating')


def convert_to_datetime(pickup_date, pickup_time):
    """ Convert string of date and time to datetime object """
    return dt.datetime.strptime(f'{pickup_date} {pickup_time}', "%Y-%m-%d %H:%M:%S")


def refresh_db(request_json=None):
    """
    Use this function to clean up the database,
    in case the data in database is not correctly shown.
    """
    if request_json is None:
        return {'message': 'no request json'}

    try:
        data = data_refresh_db_input_schema.load(request_json).get('data')
    except ValidationError:
        return {'message': 'invalid data'}

    if data is None:
        return {'message': 'Please provide data and token to access this endpoint'}

    token = data.get('token')
    is_wiped = data.get('isWiped')

    if token is None:
        return {'message': 'Unauthorized'}

    # Check for invalid token
    # is_token_invalid(token)

    if is_wiped is None:
        populate_database()
    else:
        populate_database(is_wiped)

    return {
        'message': 'Database is refreshed',
        'isWiped': is_wiped
    }


async def assign_distance(journey_list, limit=25, max_request=None):
    """ Accept list of journeys without distance and return the list with distance """
    print(f'Assign distance for {len(journey_list)} journey(s)')
    if journey_list is None:
        return journey_list

    # List to contain the return value, a counter to know the limit
    # through length of wait group list
    # journey_distance_list = []
    journey_wait_group = []
    wait_group_index = 0
    journey_wait_group.append([])

    for i, journey in enumerate(journey_list):
        # Ignore 0 value because it means the data is invalid
        # but still add it into return list
        if (journey.distance is not None
            or journey.pickup_latitude == 0
            or journey.pickup_longitude == 0
            or journey.dropoff_latitude == 0
                or journey.dropoff_longitude == 0):
            # journey_distance_list.append(journey)
            continue

        journey_wait_group[wait_group_index].append(journey)

        # Call to calculate the distance
        # when the wait group is already over the limit
        # or it reaches the last index
        if len(journey_wait_group[wait_group_index]) >= limit or i == len(journey_list) - 1:
            # increment the wait group index
            wait_group_index += 1
            journey_wait_group.append([])
            # make request to get the distance
            # distance = make_request_distance(journey_wait_group)
            # for journey_with_distance in distance:
            #     journey_distance_list.append(journey_with_distance)

    await asyncio.gather(*[run_request_distance(journey_wg_list) for journey_wg_list in journey_wait_group])
        
    # return journey_distance_list


async def run_request_distance(journey_list):
    journey_with_distance = await make_request_distance(journey_list)

    print(f'journey list {journey_list}')
    print(f'journey with distance {journey_with_distance}')

    if len(journey_with_distance) > 0:
        db.session.bulk_save_objects(journey_with_distance)
        db.session.commit()


async def make_request_distance(journey_list):
    """
    Make http request to the map service provider to calculate the distance.

    Get the dropoff and pickup location from each journey in journey list
    and then pass it as locations in the request body to get the distance
    """
    print(f'Making journey request for {len(journey_list)}')
    location_list = []
    for journey in journey_list:
        pickup_location = {
            'latLng': {
                'lat': journey.pickup_latitude,
                'lng': journey.pickup_longitude
            }
        }
        dropoff_location = {
            'latLng': {
                'lat': journey.dropoff_latitude,
                'lng': journey.dropoff_longitude
            }
        }
        location_list.append(pickup_location)
        location_list.append(dropoff_location)

    # Get the api key from config
    # and if it's none, don't bother make request
    api_key = current_app.config['MAPQUEST_API_KEY']
    if api_key is None:
        print('[ERROR]: No MAP API Key')
        return journey_list

    print('Sending request')
    payload = {'key': api_key}
    body = {'locations': location_list, 'options': 'k'}

    async with ClientSession() as session:
        req = await session.post('http://www.mapquestapi.com/directions/v2/route',
                            json=body, params=payload)
        # req = requests.post('http://www.mapquestapi.com/directions/v2/route',
        #                     json=body, params=payload)

        # validate the response using schema
        try:
            print('Dumping response json')
            response_body = response_body_schema.dump(await req.json())
        except ValidationError:
            print(f'Fail to get distance for {len(journey_list)} of journey(s)')
            return journey_list
        except JSONDecodeError:
            print(f'Fail to get distance for {len(journey_list)} of journey(s)')
            return journey_list

        legs = response_body.get('route').get('legs')

        if legs is None:
            print('[ERROR] distance cannot be calculated')
            return journey_list

        for i, leg in enumerate(legs):
            if i % 2 == 0:
                journey_list[int(i/2)].distance = float(leg.get('distance'))
                print(f"{journey_list[int(i/2)]} is updated")

    return journey_list
