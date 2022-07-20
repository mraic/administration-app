import pytest
from faker import Faker

from src import Gallery


@pytest.fixture(scope="class")
def dummy_gallery(request):
    fake = Faker()

    request.cls.dummy_gallery = Gallery(
        main_photo=fake.pystr(),
        path=fake.pystr(),
        items_id=fake.uuid4()
    )

    return request.cls.dummy_gallery


@pytest.fixture(scope="class")
@pytest.mark.usefixtures('dummy_gallery')
def create_gallery(client, dummy_gallery, dummy_item, request):
    json_data = {
        "main_photo": dummy_gallery.main_photo,
        "path": dummy_gallery.path,
        "items_id": "4c4e8715-7516-4a95-b8b9-13e6956101be"
    }

    response = client.post(
        "/gallery",
        json=json_data,
        headers={
            "Content-Type": "application/json"
        }
    )

    request.cls.create_gallery = response
