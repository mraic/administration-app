from marshmallow import fields
from marshmallow.validate import Length
from marshmallow_enum import EnumField

from src import Subcategory
from src.views import BaseSchema


class SubcategorySchema(BaseSchema):
    id = fields.UUID(dump_only=True)
    category_id = fields.UUID(required=True)
    name = fields.String(required=True, validate=Length(min=5, max=30))
    subcategory_icon = fields.String(required=True,
                                     validate=Length(min=5, max=30))
    status = EnumField(Subcategory.STATUSES, by_value=True, dump_only=True)
    state = EnumField(Subcategory.STATES, by_value=True, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ResponseOneSubcategorySchema(BaseSchema):
    data = fields.Nested("SubcategorySchema", dump_only=True)
    message = fields.String(dump_only=True)


class UpdateSubcategorySchema(SubcategorySchema):
    class Meta:
        items = fields.Nested("BaseSchema", dump_only=True)
        message = fields.String(dump_only=True)
        fields = ('name', 'subcategory_icon', 'category_id')


class SubcategoryFilterSchema(BaseSchema):
    name = fields.Nested("OperatorSchema", required=False)


class SubcategoryFilterRequestSchema(BaseSchema):
    filter_data = fields.Nested("SubcategoryFilterSchema", required=False)
    paginate_data = fields.Nested("PaginationSchema", required=True)


class GetAllSubcategoryPaginationDataSchema(BaseSchema):
    items = fields.Nested("SubcategorySchema", many=True, dump_only=True)
    total = fields.Int(dump_only=True)


class GetAllSubcategoryPaginateSchema(BaseSchema):
    data = fields.Nested("GetAllSubcategoryPaginationDataSchema",
                         dump_only=True)
    message = fields.String(dump_only=True)


class AutoCompleteSchema(BaseSchema):
    search = fields.String(required=True)


class ResponseSubcategoryManySchema(BaseSchema):
    data = fields.Nested("SubcategorySchema", many=True, dump_only=True)
    message = fields.String(dump_only=True)


create_subcategory = SubcategorySchema()
response_one_subcategory_schema = ResponseOneSubcategorySchema()
update_subcategory_schema = UpdateSubcategorySchema()
request_subcategory_filter_schema = SubcategoryFilterSchema()
get_all_subcategory_data = GetAllSubcategoryPaginateSchema()
auto_complete_schema = AutoCompleteSchema()
response_subcategory_many_schema = ResponseSubcategoryManySchema()