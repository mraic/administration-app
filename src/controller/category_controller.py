from flask_apispec import doc, use_kwargs, marshal_with

from src import bpp, Category
from src.domain.category_service import CategoryService
from src.general import Status
from src.views.category_schema import category_schema, \
    category_response_one_schema, update_category_schema, \
    request_category_filter_schema, get_all_category_data, auto_complete_schema, \
    response_category_many_schema
from src.views.message_schema import message_response_schema


@doc(description='Get category route', tags=['Category'])
@bpp.get('/categories/<uuid:category_id>')
@marshal_with(category_response_one_schema, 200, apply=True)
@marshal_with(message_response_schema, 400, apply=True)
def get_categories(category_id):
    category_service = CategoryService.get_one_by_id(_id=category_id)
    return dict(data=category_service.category,
                 message=Status.successfully_processed().message)


@doc(description='Create category route', tags=['Category'])
@bpp.post('/categories')
@use_kwargs(category_schema, apply=True)
@marshal_with(category_response_one_schema, 200, apply=True)
@marshal_with(message_response_schema, 400, apply=True)
def create_category(**kwargs):
    category_service = CategoryService(
        category=Category(
            name=kwargs.get('name'),
            category_icon=kwargs.get('category_icon')
        )
    )

    status = category_service.create()

    return dict(message=status.message, data=category_service.category)


@doc(description='Alter category route', tags=['Category'])
@bpp.put('/categories/<uuid:category_id>')
@use_kwargs(update_category_schema, apply=True)
@marshal_with(category_response_one_schema, 200, apply=True)
@marshal_with(message_response_schema, 400, apply=True)
def alter_category(category_id, **kwargs):
    category_service = CategoryService(
        category=Category(
            id=category_id,
            name=kwargs.get('name'),
            category_icon=kwargs.get('category_icon')
        )
    )

    status = category_service.alter()

    return dict(message=status.message, data=category_service.category)


@doc(description='Delete category route', tags=['Category'])
@bpp.delete('/categories/<uuid:category_id>')
@marshal_with(category_response_one_schema, 200, apply=True)
@marshal_with(message_response_schema, 400, apply=True)
def delete_category(category_id):
    category_service = CategoryService(category=Category(id=category_id))
    status = category_service.delete()

    return dict(message=status.message, data=category_service.category)


@doc(description='Activate category route', tags=['Category'])
@bpp.post('/categories/activate/<uuid:category_id>')
@marshal_with(category_response_one_schema, 200, apply=True)
@marshal_with(message_response_schema, 400, apply=True)
def activate_category(category_id):
    category_service = CategoryService(category=Category(id=category_id))
    status = category_service.activate()

    return dict(message=status.message, data=category_service.category)


@doc(description='Deactivate category route', tags=['Category'])
@bpp.post('/categories/deactivate/<uuid:category_id>')
@marshal_with(category_response_one_schema, 200, apply=True)
@marshal_with(message_response_schema, 400, apply=True)
def deactivate_category(category_id):
    category_service = CategoryService(category=Category(id=category_id))
    status = category_service.deactivate()

    return dict(message=status.message, data=category_service.category)


@doc(description='Paginate category route', tags=['Category'])
@bpp.post('/category/paginate')
@use_kwargs(request_category_filter_schema, apply=True)
@marshal_with(get_all_category_data, 200, apply=True)
@marshal_with(message_response_schema, 400, apply=True)
def get_category(**kwargs):
    filter_data = kwargs.get('filter_data')
    paginate_data = kwargs.get('paginate_data')

    items, total, status = CategoryService.get_all_categories(
        filter_data=filter_data, paginate_data=paginate_data
    )

    return dict(data=dict(items=items, total=total),
                status=status.message)


@doc(description='Autocomplete category route', tags=['Category'])
@bpp.post('/category/autocomplete')
@use_kwargs(auto_complete_schema, apply=True)
@marshal_with(response_category_many_schema, 200, apply=True)
@marshal_with(message_response_schema, 400, apply=True)
def autocomplete(**kwargs):
    data, status = CategoryService.autocomplete(search=kwargs.get('search'))

    return dict(data=data, message=status.message)
