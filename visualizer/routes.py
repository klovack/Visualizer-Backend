""" File to manage routes """
from flask import Blueprint
from flask_restx import Api, Resource

api_blueprint = Blueprint("api", __name__, url_prefix='/api')
api = Api(api_blueprint, doc="/docs")


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
