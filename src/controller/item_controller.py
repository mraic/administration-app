from flask import request
from flask_apispec import doc, use_kwargs, marshal_with

from src import bpp, Item
from src.domain.item_service import ItemService
from src.general import Status
from src.views.item_schema import item_response_one_schema, create_item_schema, \
    update_item_schema, request_item_filter_schema, get_all_items_schema, \
    auto_complete_schema, response_item_many_schema
from src.views.message_schema import message_response_schema


@doc(description='Get item route', tags=['Item'])
@bpp.get('/items/<uuid:item_id>')
@marshal_with(item_response_one_schema, 200, apply=True)
@marshal_with(message_response_schema, 400, apply=True)
def get_item_by_id(item_id):
    item_service = ItemService.get_one_by_id(_id=item_id)
    item_service.get(_id=item_id)
    return dict(data=item_service.item, message=Status.successfully_processed())


@doc(description='Create item route', tags=['Item'])
@bpp.post('/items')
@use_kwargs(create_item_schema, 'form', apply=True)
@marshal_with(item_response_one_schema, 200, apply=True)
@marshal_with(message_response_schema, 400, apply=True)
def create_item(**kwargs):
    data = ItemService.create_with_gallery(
        params=kwargs,
        file=request.files.get('file')
    )
    return data


@doc(description='Alter item route', tags=['Item'])
@bpp.put('/items/<uuid:item_id>')
@use_kwargs(update_item_schema, 'form', apply=True)
@marshal_with(item_response_one_schema, 200, apply=True)
@marshal_with(message_response_schema, 400, apply=True)
def alter_item(item_id, **kwargs):
    ItemService.alter_with_gallery(
        _id=item_id,
        params=kwargs,
        file=request.files.get('file'))

    return Status.successfully_processed()


@doc(description='Activate item route', tags=['Item'])
@bpp.post('/items/activate/<uuid:item_id>')
@marshal_with(item_response_one_schema, 200, apply=True)
@marshal_with(message_response_schema, 400, apply=True)
def activate_item(item_id):
    item_service = ItemService(item=Item(id=item_id))
    status = item_service.activate()

    return dict(message=status.message, data=item_service.item)


@doc(description='Deactivate item route', tags=['Item'])
@bpp.post('/items/deactivate/<uuid:item_id>')
@marshal_with(item_response_one_schema, 200, apply=True)
@marshal_with(message_response_schema, 400, apply=True)
def deactivate_item(item_id):
    item_service = ItemService(item=Item(id=item_id))
    status = item_service.deactivate()

    return dict(message=status.message, data=item_service.item)


@doc(description='Item paginate route', tags=['Item'])
@bpp.post('/items/paginate/')
@use_kwargs(request_item_filter_schema, apply=True)
@marshal_with(get_all_items_schema, 200, apply=True)
@marshal_with(message_response_schema, 400, apply=True)
def item_paginate(**kwargs):
    filter_data = kwargs.get('filter_data')
    paginate_data = kwargs.get('paginate_data')

    items, total, status = ItemService.get_all_items(
        filter_data=filter_data, paginate_data=paginate_data
    )

    return dict(data=dict(items=items, total=total),
                status=status.message)


@doc(description='Autocomplete item route', tags=['Item'])
@bpp.post('/items/autocomplete')
@use_kwargs(auto_complete_schema, apply=True)
@marshal_with(response_item_many_schema, 200, apply=True)
@marshal_with(message_response_schema, 400, apply=True)
def item_autocomplete(**kwargs):
    data, status = ItemService.autocomplete(search=kwargs.get('search'))

    return dict(data=data, message=status.message)
