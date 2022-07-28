import json

import pytest
from faker import Faker

from src import Item


@pytest.fixture(scope="class")
def dummy_item(request):
    fake = Faker()

    request.cls.dummy_item = Item(
        id=fake.uuid4(),
        name=fake.pystr(),
        description=fake.pystr(),
        price=fake.unique.random_int(min=1, max=999),
    )

    return request.cls.dummy_item


@pytest.fixture(scope="class")
def create_item(client, create_subcategory, dummy_item, request):
    create_subcategory_data = json.loads(create_subcategory.data)
    json_data = {
        "name": dummy_item.name,
        "description": dummy_item.description,
        "price": dummy_item.price,
        "condition_id": '737da853-e96a-4f38-8be8-37f7c1c2c0c9',
        "subcategory_id": create_subcategory_data['data']['id'],
        "file": None
    }
    response = client.post(
        "/items",
        data=json_data,
        headers={
            "Content-Type": 'multipart/form-data'
        }
    )
    request.cls.create_item = response

    return request.cls.create_item
