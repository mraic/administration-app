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
def create_item(client, dummy_item, request):

    json_data = {
        "name": dummy_item.name,
        "description": dummy_item.description,
        "price": dummy_item.price,
        "condition_id": '765cb93b-2656-46ce-8ecf-c53ba9cd84e4',
        "subcategory_id": '4c4e8715-7516-4a95-b8b9-13e6956101be',
    }

    response = client.post(
        "/items",
        data=json_data,
        headers={
            "Content-Type": 'multipart/form-data'
        }
    )

    request.cls.create_item = response
