""" File to manage routes """
from flask import Blueprint, request
from flask_restx import Api, Resource

from .services.database import refresh_db
from .services.statistic import get_statistics, get_vendors, get_vendor

api_blueprint = Blueprint("api", __name__, url_prefix='/api')
api = Api(api_blueprint, doc="/docs")

protected_ns = api.namespace('Database', path="/db",
                             description="Database operation. It's strictly forbidden to use this")
statistic_ns = api.namespace('Statistics', path="/statistics",
                             description="Endpoint to get the statistics")


@protected_ns.route('/refresh-db')
class RefreshDB(Resource):
    """ An api to refresh the database """

    def post(self):
        """ A post endpoint to refresh the database """
        return refresh_db(request_json=request.json)


@statistic_ns.route('/')
class Statistics(Resource):
    """ Statistics API Endpoint"""

    @statistic_ns.param('vendor_ids', 'List of vendor ids as array')
    @statistic_ns.param('time_start', 'Start of time, default none')
    @statistic_ns.param('time_end', 'End of time')
    @statistic_ns.param('limit', 'Limit of the data to be fetched')
    def get(self):
        """ GET Method returns the statistics of the application """
        stat = get_statistics(request.args)
        stat.update(get_vendors())
        if 'error' in stat:
            return stat, 400

        return stat, 200


@statistic_ns.route('/vendors', '/vendors/<int:vendor_id>')
class Vendors(Resource):
    """ Vendors API Endpoint """

    def get(self, vendor_id=None):
        """ 
        GET Method takes vendor_id as an argument
        if it is empty then it will return all vendors
        """
        if vendor_id is None:
            return get_vendors()
        else:
            return get_vendor(vendor_id)
