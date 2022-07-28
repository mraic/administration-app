import json

import pytest
from faker import Faker

from src import Subcategory


@pytest.fixture(scope="class")
def dummy_subcategory(request):
    fake = Faker()

    request.cls.dummy_subcategory = Subcategory(
        id=fake.uuid4(),
        name=fake.pystr(),
        subcategory_icon=fake.pystr()
    )

    return request.cls.dummy_subcategory


@pytest.fixture(scope="class")
@pytest.mark.usefixtures('dummy_category')
def create_subcategory(
        client, create_category, dummy_subcategory, dummy_category, request):
    create_category_data = json.loads(create_category.data)
    json_data = {
        "name": dummy_subcategory.name,
        "subcategory_icon": dummy_subcategory.subcategory_icon,
        "category_id": create_category_data['data']['id']
    }

    response = client.post(
        "/subcategory",
        json=json_data,
        headers={
            "Content-Type": "application/json"
        }
    )
    request.cls.create_subcategory = response

    return request.cls.create_subcategory
