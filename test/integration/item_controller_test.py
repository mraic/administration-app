import json

import pytest

from src.general import Status


@pytest.mark.usefixtures('create_item')
class TestItemController:

    @pytest.mark.run(order=1)
    def test_create_item(self):
        assert self.create_item.status_code == 200
        response_data = json.loads(self.create_item.data)
        assert 'data' in response_data
        assert 'message' in response_data
        assert response_data['message'] == \
               Status.successfully_processed().message

    @pytest.mark.run(order=2)
    def test_exits_fail(self, client):
        json_data = {}

        response = client.post(
            "/items",
            json=json_data,
            headers={
                "Content-Type": "application/json"
            }
        )

        assert response.status_code == 422
        response_data = json.loads(response.data)
        assert 'message' in response_data
        assert 'errors' in response_data

    @pytest.mark.run(order=3)
    def test_get_item(self, client):
        response_data = json.loads(self.create_item.data)

        response = client.get(
            "/items/{}".format(response_data['data']['id']),
            headers={
                "Content-Type": "multipart/form-data"
            }
        )

        get_response_data = json.loads(response.data)
        assert 'data' in get_response_data
        assert 'message' in get_response_data
        assert response_data['message'] == \
               Status.successfully_processed().message

    @pytest.mark.run(order=4)
    def test_activate_item(self, client):
        response_data = json.loads(self.create_item.data)

        from src import db
        from src import Item

        x = db.session.query(Item).filter(
            Item.id == response_data['data']['id']).first()
        x.state = Item.STATES.inactive
        x.status = Item.STATUSES.active

        response = client.post(
            "/items/activate/{}".format(response_data['data']['id']),
            headers={
                "Content-Type": "multipart/form-data"
            }
        )

        post_response_data = json.loads(response.data)
        assert 'data' in post_response_data
        assert 'message' in post_response_data
        assert post_response_data['message'] == \
               Status.successfully_processed().message
        assert post_response_data['data'][
                   'status'] == Item.STATUSES.active.value

    @pytest.mark.run(order=5)
    def test_deactivate_item(self, client):
        response_data = json.loads(self.create_item.data)

        from src import db, Item

        x = db.session.query(Item).filter(
            Item.id == response_data['data']['id']).first()
        x.status = Item.STATUSES.active

        response = client.post(
            "/items/deactivate/{}".format(response_data['data']['id']),
            headers={
                "Content-Type": ""
            }
        )

        post_response_data = json.loads(response.data)
        assert 'data' in post_response_data
        assert 'message' in post_response_data
        assert post_response_data['message'] == \
               Status.successfully_processed().message
        assert post_response_data['data'][
                   'status'] == Item.STATUSES.active.value

    @pytest.mark.run(order=6)
    def test_item_paginate(self, client):
        response_data = json.loads(self.create_item.data)

        json_data = {
            "filter_data": {
                "name": {
                    "operator": "CONTAINS",
                    "value": ""
                }
            },
            "paginate_data": {

                "length": 10,
                "start": 1
            }
        }

        response = client.post(
            "/items/paginate/",
            data=json_data,
            headers={
                "Content-Type": "multipart/form-data"
            }
        )

        post_paginate_data = json.loads(response.data)
        assert 'data' in post_paginate_data
        assert post_paginate_data['data']['total'] > 0
        assert response.status_code == 200
