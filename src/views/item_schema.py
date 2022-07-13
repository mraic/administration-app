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
    condition_id = fields.UUID(required=True)
    state = EnumField(Item.STATES, by_value=True, dump_only=True)
    status = EnumField(Item.STATUSES, by_value=True, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    subcategory_id = fields.UUID(required=True)
    category_id = fields.UUID(dump_only=True)
    file = fields.Raw(type='file', required=False, allow_none=True)

class ItemFullSchema(ItemSchema):
    subcategory = fields.Nested("SubcategorySchema")
    category = fields.Nested("CategorySchema")
    gallery = fields.Nested("GallerySchema")


class ItemResponseSchema(BaseSchema):
    data = fields.Nested("ItemFullSchema", dump_only=True)
    message = fields.String(dump_only=True)


class UpdateItemSchema(ItemSchema):
    class Meta:
        items = fields.Nested("BaseSchema", dump_only=True)
        message = fields.String(dump_only=True)
        fields = ('name', 'description', 'price', 'condition_id')


class AutoCompleteSchema(BaseSchema):
    search = fields.String(required=True)


class ResponseItemManySchema(BaseSchema):
    data = fields.Nested("ItemFullSchema", many=True, dump_only=True)
    message = fields.String(dump_only=True)


class ItemFilterSchema(BaseSchema):
    name = fields.Nested("OperatorSchema", required=False)
    price = fields.Nested("FromToSchema", required=False)
    date = fields.Nested("DateFromToSchema", required=False)
    condition_id = fields.UUID(required=False, allow_none=True)


class RequestFilterItemSchema(BaseSchema):
    filter_data = fields.Nested("ItemFilterSchema", required=False)
    paginate_data = fields.Nested("PaginationSchema", required=False)


class GetAllItemsPaginateDataSchema(BaseSchema):
    items = fields.Nested("ItemSchema", many=True, dump_only=True)
    total = fields.Int(dump_only=True)


class GetAllItemsSchema(BaseSchema):
    data = fields.Nested("GetAllItemsPaginateDataSchema", dump_only=True)
    message = fields.String(dump_only=True)


create_item_schema = ItemSchema()
item_response_one_schema = ItemResponseSchema()
update_item_schema = UpdateItemSchema()
auto_complete_schema = AutoCompleteSchema()
response_item_many_schema = ResponseItemManySchema()
request_item_filter_schema = RequestFilterItemSchema()
get_all_items_schema = GetAllItemsSchema()
