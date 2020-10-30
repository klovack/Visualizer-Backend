""" A model to define the request schema for statistic route """

import datetime

from marshmallow import fields
from .. import marshmallow as ma


class StatisticParamSchema(ma.Schema):
    """ Schema for statistics route """
    vendor_ids: fields.List(fields.String)
    time_start: fields.DateTime()
    time_end: fields.DateTime()
    limit: fields.Integer()


statistic_param_schema = StatisticParamSchema()


def convert_multi_dict_to_statistic_param(multi_dict):
    """ Convert multidict to statistics param dict """
    if multi_dict is None:
        return {}

    result = {}

    if 'vendor_ids' in multi_dict:
        result['vendor_ids'] = multi_dict.getlist('vendor_ids')

    if 'timeStart' in multi_dict:
        result['time_start'] = datetime.datetime.strptime(
            multi_dict.get('timeStart'), "%Y-%m-%dT%H:%M")

    if 'timeEnd' in multi_dict:
        result['time_end'] = datetime.datetime.strptime(
            multi_dict.get('timeEnd'), "%Y-%m-%dT%H:%M")

    if 'limit' in multi_dict:
        result['limit'] = multi_dict.get('limit')

    return result
