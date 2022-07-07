from flask_apispec import doc, use_kwargs, marshal_with

from src import bpp, Subcategory
from src.domain.subcategory_service import SubcategoryService

from src.views.message_schema import message_response_schema
from src.views.subcategory_schema import response_one_subcategory_schema, \
    create_subcategory, update_subcategory_schema, \
    response_subcategory_many_schema, auto_complete_schema, \
    request_subcategory_filter_schema, get_all_subcategory_data


@doc(description="Create subcategory route", tags=['Subcategory'])
@bpp.post('/subcategory')
@use_kwargs(create_subcategory, apply=True)
@marshal_with(response_one_subcategory_schema, 200, apply=True)
@marshal_with(message_response_schema, 400, apply=True)
def create_subcategory(**kwargs):
    subcategory_service = SubcategoryService(
        subcategory=Subcategory(
            name=kwargs.get('name'),
            subcategory_icon=kwargs.get('subcategory_icon'),
            category_id=kwargs.get('category_id')
        )
    )

    status = subcategory_service.create()

    return dict(message=status.message, data=subcategory_service.subcategory)


@doc(description='Alter subcategory route', tags=['Subcategory'])
@bpp.put('/subcategory/<uuid:subcategory_id>')
@use_kwargs(update_subcategory_schema, apply=True)
@marshal_with(response_one_subcategory_schema, 200, apply=True)
@marshal_with(message_response_schema, 400, apply=True)
def alter_subcategory(subcategory_id, **kwargs):
    subcategory_service = SubcategoryService(
        subcategory=Subcategory(
            id=subcategory_id,
            name=kwargs.get('name'),
            subcategory_icon=kwargs.get('subcategory_icon'),
            category_id=kwargs.get('category_id')
        )
    )

    status = subcategory_service.alter()

    return dict(message=status.message, data=subcategory_service.subcategory)


@doc(description='Delete subcategory route', tags=['Subcategory'])
@bpp.delete('/subcategory/<uuid:subcategory_id>')
@marshal_with(response_one_subcategory_schema, 200, apply=True)
@marshal_with(message_response_schema, 400, apply=True)
def delete_subcategory(subcategory_id):
    subcategory_service = SubcategoryService(
        subcategory=Subcategory(id=subcategory_id)
    )

    status = subcategory_service.delete(_id=subcategory_id)

    return dict(message=status.message, data=subcategory_service.subcategory)


@doc(description='Activate category route', tags=['Subcategory'])
@bpp.post('/subcategories/activate/<uuid:subcategory_id>')
@marshal_with(response_one_subcategory_schema, 200, apply=True)
@marshal_with(message_response_schema, 400, apply=True)
def activate_subcategory(subcategory_id):
    subcategory_service = SubcategoryService(
        subcategory=Subcategory(id=subcategory_id))
    status = subcategory_service.activate(_id=subcategory_id)

    return dict(message=status.message, data=subcategory_service.subcategory)


@doc(description='Deactivate category route', tags=['Subcategory'])
@bpp.post('/subcategories/deactivate/<uuid:subcategory_id>')
@marshal_with(response_one_subcategory_schema, 200, apply=True)
@marshal_with(message_response_schema, 400, apply=True)
def deactivate_subcategory(subcategory_id):
    subcategory_service = SubcategoryService(
        subcategory=Subcategory(id=subcategory_id))
    status = subcategory_service.deactivate(_id=subcategory_id)

    return dict(message=status.message, data=subcategory_service.subcategory)


@doc(description='Paginate category route', tags=['Subcategory'])
@bpp.post('/subcategory/paginate')
@use_kwargs(request_subcategory_filter_schema, apply=True)
@marshal_with(get_all_subcategory_data, 200, apply=True)
@marshal_with(message_response_schema, 400, apply=True)
def get_subcategory(**kwargs):

    filter_data = kwargs.get('filter_data')
    paginate_data = kwargs.get('paginate_data')

    items, total, status = SubcategoryService.get_all_subcategories(
        filter_data=filter_data, paginate_data=paginate_data
    )

    return dict(data=dict(items=items, total=total),
                status=status.message)


@doc(description='Autocomplete category route', tags=['Subcategory'])
@bpp.post('/subcategory/autocomplete')
@use_kwargs(auto_complete_schema, apply=True)
@marshal_with(response_subcategory_many_schema, 200, apply=True)
@marshal_with(message_response_schema, 400, apply=True)
def autocomplete_subcategory(**kwargs):
    data, status = SubcategoryService.autocomplete(search=kwargs.get('search'))

    return dict(data=data, message=status.message)
