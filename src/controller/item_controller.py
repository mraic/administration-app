from flask_apispec import doc, use_kwargs, marshal_with

from src import bpp, Item
from src.domain.item_service import ItemService
from src.views.item_schema import item_response_one_schema, create_item_schema, \
    update_item_schema, auto_complete_schema, response_item_many_schema
from src.views.message_schema import message_response_schema


@doc(description='Create item route', tags=['Item'])
@bpp.post('/items')
@use_kwargs(create_item_schema, apply=True)
@marshal_with(item_response_one_schema, 200, apply=True)
@marshal_with(message_response_schema, 400, apply=True)
def create_item(**kwargs):
    item_service = ItemService(
        item=Item(
            name=kwargs.get('name'),
            description=kwargs.get('description'),
            price=kwargs.get('price'),
            condition=kwargs.get('condition'),
            subcategory_id=kwargs.get('subcategory_id')
        )
    )

    status = item_service.create()

    return dict(message=status.message, data=item_service.item)


@doc(description='Alter item route', tags=['Item'])
@bpp.put('/items/<uuid:item_id>')
@use_kwargs(update_item_schema, apply=True)
@marshal_with(item_response_one_schema, 200, apply=True)
@marshal_with(message_response_schema, 400, apply=True)
def alter_item(item_id, **kwargs):
    item_service = ItemService(
        item=Item(
            id=item_id,
            name=kwargs.get('name'),
            description=kwargs.get('description'),
            price=kwargs.get('price'),
            condition=kwargs.get('condition'),
        )
    )

    status = item_service.alter()

    return dict(message=status.message, data=item_service.item)


@doc(description='Activate item route', tags=['Item'])
@bpp.post('/items/activate/<uuid:category_id>')
@marshal_with(item_response_one_schema, 200, apply=True)
@marshal_with(message_response_schema, 400, apply=True)
def activate_item(item_id):
    item_service = ItemService(item=Item(id=item_id))
    status = item_service.activate(_id=item_id)

    return dict(message=status.message, data=item_service.item)


@doc(description='Deactivate item route', tags=['Item'])
@bpp.post('/items/deactivate/<uuid:item_id>')
@marshal_with(item_response_one_schema, 200, apply=True)
@marshal_with(message_response_schema, 400, apply=True)
def deactivate_item(item_id):
    item_service = ItemService(item=Item(id=item_id))
    status = item_service.deactivate(_id=item_id)

    return dict(message=status.message, data=item_service.item)


@doc(description='Autocomplete item route', tags=['Item'])
@bpp.post('/items/autocomplete')
@use_kwargs(auto_complete_schema, apply=True)
@marshal_with(response_item_many_schema, 200, apply=True)
@marshal_with(message_response_schema, 400, apply=True)
def item_autocomplete(**kwargs):
    data, status = ItemService.autocomplete(search=kwargs.get('search'))

    return dict(data=data, message=status.message)
