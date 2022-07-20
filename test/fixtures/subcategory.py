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
def create_subcategory(client, dummy_subcategory, dummy_category, request):
    json_data = {
        "name": dummy_subcategory.name,
        "subcategory_icon": dummy_subcategory.subcategory_icon,
        "category_id": "59dc8d86-d5ce-4aea-88b3-75d1744ab6ed"
    }

    response = client.post(
        "/subcategory",
        json=json_data,
        headers={
            "Content-Type": "application/json"
        }
    )

    request.cls.create_subcategory = response
