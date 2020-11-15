""" 
A Configuration file to be used by flask
"""
import os

SQLALCHEMY_DATABASE_URI='postgresql://postgres:my-secret-password@database:5432/visualizer-dev'
SQLALCHEMY_TRACK_MODIFICATIONS=True

REDIS_URL='redis://redis:6379/0'

FRONTEND_URI='http://localhost:3000'

# An API Key which you can get at
# https://developer.mapquest.com
MAPQUEST_API_KEY=os.getenv('MAPQUEST_API_KEY')
MAPQUEST_LIMIT_REQUEST=25

GOOGLE_CLIENT_ID=os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET=os.getenv('GOOGLE_CLIENT_SECRET')

ORIGINS=[
  'http://localhost:3000',  # React
  'http://127.0.0.1:3000',  # React
]
CORS_SUPPORTS_CREDENTIALS=True
