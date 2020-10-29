""" 
A Configuration file to be used by flask
"""
# from .secret import MAP_QUEST_API

SQLALCHEMY_DATABASE_URI='postgresql://postgres:my-secret-password@localhost:5432/visualizer-dev'
SQLALCHEMY_TRACK_MODIFICATIONS=True

# An API Key which you can get at
# https://developer.mapquest.com
MAPQUEST_API_KEY='your-secret-api-key'
MAPQUEST_LIMIT_REQUEST=30
