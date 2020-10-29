""" This module contains schema for interacting with mapquest """

from marshmallow import fields
from .. import marshmallow


class LatLngSchema(marshmallow.Schema):
    lat = fields.Float()
    lng = fields.Float()


class MapQuestLocationsSchema(marshmallow.Schema):
    latLng = fields.Nested(LatLngSchema)


class MapQuestOptionsSchema(marshmallow.Schema):
    unit = fields.String()
    locale = fields.String()


class MapQuestRequestBodySchema(marshmallow.Schema):
    locations = fields.List(fields.Dict)
    options = fields.Nested(MapQuestOptionsSchema)


class MapQuestLegSchema(marshmallow.Schema):
    distance = fields.Float()
    formattedTime = fields.String()


class MapQuestRouteSchema(marshmallow.Schema):
    legs = fields.List(fields.Dict)


class MapQuestInfoSchema(marshmallow.Schema):
    statuscode = fields.Number()


class MapQuestResponseBodySchema(marshmallow.Schema):
    route = fields.Nested(MapQuestRouteSchema)
    info = fields.Nested(MapQuestInfoSchema)


response_body_schema = MapQuestResponseBodySchema()
request_body_schema = MapQuestRequestBodySchema()
