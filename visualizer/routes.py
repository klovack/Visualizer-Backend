""" File to manage routes """
import json

from flask import Blueprint, request, url_for, session, redirect, current_app, Response, make_response
from flask_restx import Api, Resource
from functools import wraps

from . import oauth, redis_client
from .services.database import refresh_db
from .services.statistic import get_statistics, get_vendors, get_vendor

api_blueprint = Blueprint("api", __name__, url_prefix='/api')
api = Api(api_blueprint, doc="/docs")

protected_ns = api.namespace('Database', path="/db",
                             description="Database operation. It's strictly forbidden to use this")
statistic_ns = api.namespace('Statistics', path="/statistics",
                             description="Endpoint to get the statistics")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'Authorization' not in request.headers:
            return {
                'error': 'user not logged in',
                'message': 'You can log in via /api/login?oauth_provider=<your-oauth-provide>',
                'availableOauth': [
                    'google',
                    'facebook',
                    'github'
                ]
            }, 401
        
        # Check if the user exist in reddit
        access_token = request.headers['Authorization']
        auth_token_str = redis_client.get(access_token)

        if auth_token_str is None:
            return {
                'error': 'token is invalid',
                'message': 'Unauthorized access because token is invalid'
            }, 401
        
        auth_token = json.loads(auth_token_str)

        if 'google' in access_token:
            user = oauth.google.parse_id_token(auth_token)
            if user is None:
                return {
                    'error': 'user is invalid',
                    'message': 'Provided token is invalid'
                }, 401
            
            return f(*args, **kwargs, user=user)
        
        return f(*args, **kwargs)
    return decorated_function

@api_blueprint.route('/login')
def login():
    oauth_provider = request.args.get('oauth_provider')
    if oauth_provider is None:
        redirect_uri = current_app.config['FRONTEND_URI']
        return redirect(redirect_uri)

    if oauth_provider == 'google':
        redirect_uri = url_for('api.auth', oauth_provider=oauth_provider, _external=True)
        return oauth.google.authorize_redirect(redirect_uri)

    else:
        redirect_uri = current_app.config['FRONTEND_URI']
        return redirect(redirect_uri)
    

@api_blueprint.route('/auth/<string:oauth_provider>')
def auth(oauth_provider):
    if oauth_provider == 'google':
        token = oauth.google.authorize_access_token()
        if 'access_token' in token:
            # save the token in redis and redirect the user to the frontend
            access_token = 'google-' + token['access_token']
            redis_client.set(access_token, json.dumps(token))
            redirect_uri = current_app.config['FRONTEND_URI'] + '/dashboard?token=' + access_token
            response = redirect(redirect_uri)
            return response
    return redirect(current_app.config['FRONTEND_URI'] + '?error=true')


@api_blueprint.route('/me')
@login_required
def me(user=None):
    if user is None:
        return {
            'error': "no user found",
            'message': "You either not logged in or there's no user with that access"
        }
    return user

@api_blueprint.route('/logout')
@login_required
def logout(user=None):
    redis_client.delete(request.headers['Authorization'])
    redirect_uri = current_app.config['FRONTEND_URI']
    return redirect(redirect_uri)


@protected_ns.route('/refresh-db')
class RefreshDB(Resource):
    """ An api to refresh the database """

    # @login_required
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
    # @login_required
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

    # @login_required
    def get(self, vendor_id=None):
        """ 
        GET Method takes vendor_id as an argument
        if it is empty then it will return all vendors
        """
        if vendor_id is None:
            return get_vendors()
        else:
            return get_vendor(vendor_id)
