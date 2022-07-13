import pytest
from faker import Faker

from src import Item


@pytest.fixture(scope="class")
def dummy_item(request):
    fake = Faker()

    request.cls.dummy_item = Item(
        id=fake.uuid4(),
        name=fake.pystr(),
        description = fake.pystr(),
        price=fake.unique.random_int(min=1, max=999),
    )

    return request.cls.dummy_item
