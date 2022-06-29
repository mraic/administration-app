from marshmallow import fields
from marshmallow.validate import Length
from marshmallow_enum import EnumField

from .. import Category
from ..views import BaseSchema

class CategorySchema(BaseSchema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(validate=Length(min=2, max=30))
    category_icon = fields.Str(validate=Length(min=2, max=30))
    state = EnumField(Category.STATES, by_value=True, dump_only=True)
    status = EnumField(Category.STATUSES, by_value=True, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class CategoryResponseSchema(BaseSchema):
    data = fields.Nested("CategorySchema", dump_only=True)
    message = fields.String(dump_only=True)

category_schema = CategorySchema()
category_response_one_schema = CategoryResponseSchema()