from marshmallow import fields
from marshmallow.validate import Length
from marshmallow_enum import EnumField

from src import Item, AppLogException
from src.views import BaseSchema


def price_validator(price):
    if price < 0:
        raise AppLogException('Price must be positive')


class ItemSchema(BaseSchema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True, validate=Length(min=5, max=50))
    description = fields.Str(required=True, validate=Length(max=1000))
    price = fields.Float(required=True, validate=price_validator)
    condition = fields.Str(required=True)
    state = EnumField(Item.STATES, by_value=True, dump_only=True)
    status = EnumField(Item.STATUSES, by_value=True, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    subcategory_id = fields.UUID(required=True)


class ItemResponseSchema(BaseSchema):
    data = fields.Nested("ItemSchema", dump_only=True)
    message = fields.String(dump_only=True)


class UpdateItemSchema(ItemSchema):
    class Meta:
        items = fields.Nested("BaseSchema", dump_only=True)
        message = fields.String(dump_only=True)
        fields = ('name', 'description', 'price', 'condition')


class AutoCompleteSchema(BaseSchema):
    search = fields.String(required=True)


class ResponseItemManySchema(BaseSchema):
    data = fields.Nested("CategorySchema", many=True, dump_only=True)
    message = fields.String(dump_only=True)


create_item_schema = ItemSchema()
item_response_one_schema = ItemResponseSchema()
update_item_schema = UpdateItemSchema()
auto_complete_schema = AutoCompleteSchema()
response_item_many_schema = ResponseItemManySchema()
