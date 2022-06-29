from flask_apispec import doc, use_kwargs, marshal_with

from src import bpp, Category
from src.domain.category_service import CategoryService
from src.views.category_schema import category_schema, \
    category_response_one_schema
from src.views.message_schema import message_response_schema


@doc(description='Create category route', tags=['Category'])
@bpp.post('/categories')
@use_kwargs(category_schema, apply =True)
@marshal_with(category_response_one_schema, 200, apply=True)
@marshal_with(message_response_schema, 400, apply=True)
def create_category(**kwargs):

    category_service = CategoryService(
        category=Category(
            name = kwargs.get('name'),
            category_icon = kwargs.get('category_icon')
        )
    )

    status = category_service.create()

    return dict(message=status.message, data = category_service.category)