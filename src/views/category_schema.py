from marshmallow import fields
from marshmallow.validate import Length
from marshmallow_enum import EnumField

from .. import Category
from ..views import BaseSchema


class CategorySchema(BaseSchema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True, validate=Length(min=5, max=30))
    category_icon = fields.Str(required=True)
    state = EnumField(Category.STATES, by_value=True, dump_only=True)
    status = EnumField(Category.STATUSES, by_value=True, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    subcategory = fields.Nested("SubcategorySchema", dump_only=True, many=True)


class UpdateCategorySchema(CategorySchema):
    class Meta:
        items = fields.Nested("BaseSchema", dump_only=True)
        message = fields.String(dump_only=True)
        fields = ('name', 'category_icon', 'state', 'status')


class CategoryResponseSchema(BaseSchema):
    data = fields.Nested("CategorySchema", dump_only=True)
    message = fields.String(dump_only=True)


class ActivateCategorySchema(CategorySchema):
    class Meta:
        items = fields.Nested("BaseSchema", dump_only=True)
        message = fields.String(dum_only=True)
        fields = ('state', 'status')


class CategoryFilterSchema(BaseSchema):
    name = fields.Nested("OperatorSchema", required=False)


class CategoryFilterRequestSchema(BaseSchema):
    filter_data = fields.Nested("CategoryFilterSchema")
    paginate_data = fields.Nested("PaginationSchema")


class GetAllCategoryPaginationDataSchema(BaseSchema):
    items = fields.Nested("CategorySchema", many=True, dump_only=True)
    total = fields.Int(dump_only=True)


class GetAllCategoryPaginateSchema(BaseSchema):
    data = fields.Nested("GetAllCategoryPaginationDataSchema", dump_only=True)
    message = fields.String(dump_only=True)


class AutoCompleteSchema(BaseSchema):
    search = fields.String(required=True)


class ResponseCategoryManySchema(BaseSchema):
    data = fields.Nested("CategorySchema", many=True, dump_only=True)
    message = fields.String(dump_only=True)


class CategoryFullSchema(CategorySchema):
    subcategory = fields.Nested("SubcategorySchema")


class CategoryResponseFullSchema(BaseSchema):
    data = fields.Nested("CategoryFullSchema", many=True, dump_only=True)
    message = fields.String(dump_only=True)


category_schema = CategorySchema()
category_response_one_schema = CategoryResponseSchema()
update_category_schema = UpdateCategorySchema()
activate_category_schema = ActivateCategorySchema()
request_category_filter_schema = CategoryFilterRequestSchema()
get_all_category_data = GetAllCategoryPaginateSchema()
auto_complete_schema = AutoCompleteSchema()
response_category_many_schema = ResponseCategoryManySchema()
category_response_full_schema = CategoryResponseFullSchema()
