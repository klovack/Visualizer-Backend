""" Module to handle statistic operations """

from marshmallow.exceptions import ValidationError
from sqlalchemy import or_, text
from sqlalchemy.exc import SQLAlchemyError

from ..models.journey import Journey, journey_schema
from ..models.statistic import convert_multi_dict_to_statistic_param


def get_statistics(query_param):
    """ Get the statistic data from database based on the query param """
    try:
        queries = convert_multi_dict_to_statistic_param(query_param)

        sql_query = Journey.query

        print(queries)

        # Filter by vendor id
        if 'vendor_ids' in queries:
            sql_text = None
            for v_id in queries.get('vendor_ids'):
                if sql_text is not None:
                    sql_text = or_(sql_text, text(f'vendor_id = {v_id}'))
                else:
                    sql_text = or_(text(f'vendor_id = {v_id}'))

            if sql_text is not None:
                sql_query = sql_query.filter(sql_text)

        # Filter by time start and time end
        if 'time_start' in queries and 'time_end' in queries:
            sql_text = text(
                f'''pickup_time >= '{queries.get("time_start")}' and dropoff_time <= '{queries.get("time_end")}' ''')
            sql_query = sql_query.filter(sql_text)
        elif 'time_start' in queries:
            sql_text = text(
                f'''pickup_time >= '{queries.get("time_start")}' ''')
            sql_query = sql_query.filter(sql_text)
        elif 'time_end' in queries:
            sql_text = text(f'''pickup_time <= '{queries.get("time_end")}' ''')
            sql_query = sql_query.filter(sql_text)

        # For debug purpose
        # print(sql_query)
        res = sql_query.all()
        journeys_json = journey_schema.dump(res, many=True)

        return {
            'data': {
                'journeys': journeys_json
            }
        }
    except (ValidationError, SQLAlchemyError) as err:
        return {
            'error': {
                'code': 400,
                'message': err.messages
            }
        }
