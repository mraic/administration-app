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
