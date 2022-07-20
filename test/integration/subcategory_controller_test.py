import json

import pytest

from src.general import Status


@pytest.mark.usefixtures('create_subcategory')
class TestCategoryController:

    @pytest.mark.run(order=1)
    def test_get_subcategory(self, client):
        response_data = json.loads(self.create_subcategory.data)

        response = client.get(
            "/subcategory/{}".format(response_data['data']['id']),
            headers={
                "Content-Type": "application/json"
            }
        )

        get_response_data = json.loads(response.data)
        assert 'data' in get_response_data
        assert 'message' in get_response_data
        assert get_response_data['message'] == \
               Status.successfully_processed().message
        assert response.status_code == 200

    @pytest.mark.run(order=2)
    def test_create_subcategory(self, client):
        response_data = json.loads(self.create_subcategory.data)

        json_data = {
            "name": response_data['data']['name'],
            "subcategory_icon": response_data['data']['subcategory_icon'],
            "category_id": response_data['data']['category_id']
        }

        from src import Subcategory, db
        from faker import Faker

        fake = Faker()
        x = db.session.query(Subcategory).filter(
            Subcategory.name == response_data['data']['name']).first()

        x.name = fake.pystr()
        response = client.post(
            "/subcategory",
            json=json_data,
            headers={
                "Content-Type": "application/json"
            }
        )

        post_response_data = json.loads(response.data)
        assert 'data' in post_response_data
        assert 'message' in post_response_data
        assert post_response_data['message'] == \
               Status.successfully_processed().message
        assert response.status_code == 200

    @pytest.mark.run(order=3)
    def test_alter_subcategory(self, client):
        response_data = json.loads(self.create_subcategory.data)

        json_data = {
            "name": response_data['data']['name'],
            "subcategory_icon": response_data['data']['subcategory_icon'],
            "category_id": response_data['data']['category_id']
        }

        response = client.put(
            "/subcategory/{}".format(response_data['data']['id']),
            json=json_data,
            headers={
                "Content-Type": "application/json"
            }
        )

        put_response_data = json.loads(response.data)
        assert 'data' in put_response_data
        assert 'message' in put_response_data
        assert put_response_data['message'] == \
               Status.successfully_processed().message
        assert response.status_code == 200

    @pytest.mark.run(order=4)
    def test_delete_subcategory(self, client):
        response_data = json.loads(self.create_subcategory.data)

        response = client.delete(
            "/subcategory/{}".format(response_data['data']['id']),
            headers={
                "Content-Type": "application/json"
            }
        )

        delete_response_data = json.loads(response.data)
        assert 'data' in delete_response_data
        assert 'message' in delete_response_data
        assert delete_response_data['message'] == \
               Status.successfully_processed().message
        assert response.status_code == 200

    @pytest.mark.run(order=5)
    def test_activate_subcategory(self, client):
        from src import db, Subcategory

        response_data = json.loads(self.create_subcategory.data)

        x = db.session.query(Subcategory).filter(
            Subcategory.id == response_data['data']['id']).first()
        x.state = Subcategory.STATES.inactive
        x.status = Subcategory.STATUSES.active

        response = client.post(
            '/subcategories/activate/{}'.format(response_data['data']['id']),
            headers={
                "Content-Type": "application/json"
            }
        )

        post_response_data = json.loads(response.data)
        assert 'data' in post_response_data
        assert 'message' in post_response_data
        assert post_response_data['message'] == \
               Status.successfully_processed().message
        assert post_response_data['data']['state'] == 'active'

    @pytest.mark.run(order=6)
    def test_deactivate_subcategory(self, client):
        from src import db, Subcategory

        response_data = json.loads(self.create_subcategory.data)

        x = db.session.query(Subcategory).filter(
            Subcategory.name == response_data['data']['name']).first()
        x.status = Subcategory.STATUSES.active

        response = client.post(
            "/subcategories/deactivate/{}".format(response_data['data']['id']),
            headers={
                "Content-Type": "application/json"
            }
        )

        post_response_data = json.loads(response.data)
        assert 'data' in post_response_data
        assert 'message' in post_response_data
        assert post_response_data['message'] == \
               Status.successfully_processed().message
        assert response.status_code == 200

    @pytest.mark.run(order=7)
    def test_paginate_subcategory(self, client):
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
            "/subcategory/paginate",
            json=json_data,
            headers={
                "Content-Type": "application/json"
            }
        )

        post_paginate_date = json.loads(response.data)
        assert 'data' in post_paginate_date
        assert post_paginate_date['data']['total'] > 0
        assert response.status_code == 200
