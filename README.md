# Visualizer Server

The server is written in python using Flask framework. The database i'm using is Postgresql but it easily replacable with other SQL database.

## Problem and solutions

The csv does not come with distance, only the start and end location of the journey.
To solve this problem, a third party service is needed to calculate the distance between these 2 locations,
since creating from scratch wouldn't make sense. 

Service we'll be using is [MapQuest](https://developer.mapquest.com/).

## REST End Points

1. `GET` __/statistics__

    Should return `json` object which shows all statistics of the journey incl. distance and fares

2. `GET` __/statistics/fares__

    Should return `json` object which shows statistics of fares

3. `GET` __/statistics/distances__

    Should return `json` object which shows statistics of distance

4. `POST` __/auth__

    Should authenticate the user over oAuth and return jwt token