import pytest
from faker import Faker

from src import Category


@pytest.fixture(scope="class")
def dummy_category(request):
    fake = Faker()

    request.cls.dummy_category = Category(

        id=fake.uuid4(),
        name=fake.pystr(),
        category_icon=fake.pystr()

    )

    return request.cls.dummy_category


@pytest.fixture(scope="class")
def create_category( client, dummy_category, request):
    json_data = {
        "name": dummy_category.name,
        "category_icon": dummy_category.category_icon
    }

    response = client.post(
        "/categories",
        json=json_data,
        headers={
            "Content-Type": "application/json"
        }
    )
    request.cls.create_category = response

    return request.cls.create_category
