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
