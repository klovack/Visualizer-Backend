""" File to manage routes """
from flask import Blueprint, request
from flask_restx import Api, Resource
from marshmallow.exceptions import ValidationError

from .services.journey import populate_database
from .models import data_refresh_db_input_schema

api_blueprint = Blueprint("api", __name__, url_prefix='/api')
api = Api(api_blueprint, doc="/docs")



@api.route('/refresh-db')
class RefreshDB(Resource):
    """ An api to refresh the database """

    def post(self):
        """ A post endpoint to refresh the database """

        try:
            data = data_refresh_db_input_schema.load(request.json).get('data')
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


@api.route('/statistics')
class Statistics(Resource):
    """ Statistics Endpoint API """

    def get(self):
        """ GET Method returns the statistics of the application """
        return {'data': 'statistics'}


@api.route('/statistics/distance')
class Distance(Resource):
    """ Distance API Endpoint """

    def get(self):
        """ GET method returns distance based on the query """
        return {'data': 'distance'}


@api.route('/statistics/fares')
class Fares(Resource):
    """ Fares API Endpoint """

    def get(self):
        """ GET method returns fares based on the query """
        return {'data': 'fares'}
