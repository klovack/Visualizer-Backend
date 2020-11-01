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

2. `GET` __/api/statistics/vendors/:id__

    Should either return 1 vendor or all vendors if call without id

3. `POST` __/auth__

    Should authenticate the user over oAuth and return jwt token

For more documentation, start the app by executing `run.sh`,
just make sure, you do this steps:

1. Start python virtual env, you can do that by executing:

    ```sh
    py -m venv venv
    pip install -r requirements.txt
    ```

2. postgresql is running. You can do that by doing:

    ```
    cd db
    docker-compose up -d
    ```

and then go to

```
http://localhost:5000/api/docs
```

### NOTES

If you run the application for the first time, you need to create the database first.
To create the database, start the postgresql and then execute:

```bash
# you have to be at root application
python setup.py
```

When running it for the first time, the database will be empty. To populate the database, start the application and then go to `localhost:5000/api/db/refresh-db`.