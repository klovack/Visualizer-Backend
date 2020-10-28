""" A services to populate the journey in the database """

import datetime as dt

from marshmallow.exceptions import ValidationError

from .. import db
from ..models.journey import Journey
from ..models.vendor import Vendor
from ..models import data_refresh_db_input_schema
from .mock.tours import get_tours_data


def populate_database(refresh=False):
    """
    Function to populate the database with the data from csv file.
    Only run this once, otherwise you will have duplicate data.
    """
    print('Begin populating')

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
    journey_obj_list = list()
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

    db.session.bulk_save_objects(journey_obj_list)
    db.session.commit()
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
