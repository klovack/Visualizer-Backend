from marshmallow import fields
from .. import marshmallow

class RefreshDBInputSchema(marshmallow.Schema):
    token = fields.String(required=True)
    isWiped = fields.Boolean()

class DataRefreshDBInputSchema(marshmallow.Schema):
    data = fields.Nested(RefreshDBInputSchema)

data_refresh_db_input_schema = DataRefreshDBInputSchema()
refresh_db_input_schema = RefreshDBInputSchema()
