import pytest
from faker import Faker

from src import Gallery

@pytest.fixture(scope="class")
def dummy_gallery(request):

    fake = Faker()

    request.cls.dummy_gallery = Gallery(
        main_photo = fake.pystr(),
        path = fake.pystr(),
        items_id = fake.uuid4()
    )

    return request.cls.dummy_gallery