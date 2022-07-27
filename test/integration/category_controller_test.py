import json

import pytest

from src.general import Status


@pytest.mark.usefixtures('create_category')
class TestCategoryController:

    @pytest.mark.run(order=1)
    def test_create_category(self):
        assert self.create_category.status_code == 200
        response_data = json.loads(self.create_category.data)
        assert 'data' in response_data
        assert 'message' in response_data
        assert response_data['message'] == \
               Status.successfully_processed().message

    @pytest.mark.run(order=2)
    def test_exists_fail(self, client):
        json_data = {}

        response = client.post(
            "/categories",
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
    def test_category_delete(self, client):
        response_data = json.loads(self.create_category.data)

        response = client.delete(
            "/categories/{}".format(response_data['data']['id']),
            headers={
                "Content-Type": "application/json"
            }
        )

        delete_response_data = json.loads(response.data)
        assert 'data' in delete_response_data
        assert 'message' in delete_response_data
        assert delete_response_data['message'] == \
               Status.successfully_processed().message
        assert delete_response_data['data']['status'] == 0

    @pytest.mark.run(order=4)
    def test_get_category(self, client):
        response_data = json.loads(self.create_category.data)

        response = client.get(
            "/categories/{}".format(response_data['data']['id']),
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

    @pytest.mark.run(order=5)
    def test_alter_category(self, client):
        from src import db
        from src import Category

        response = json.loads(self.create_category.data)

        json_data = {
            "name": response['data']['name'],
            "category_icon": response['data']['category_icon']
        }
        x = db.session.query(Category).filter(
            Category.name == response['data']['name']).first()
        x.status = Category.STATUSES.active

        response = client.put(
            "/categories/{}".format(response['data']['id']),
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

    @pytest.mark.run(order=5)
    def test_category_deactivate(self, client):
        from src import db, Category
        response = json.loads(self.create_category.data)

        x = db.session.query(Category).filter(
            Category.name == response['data']['name']).first()
        x.status = Category.STATUSES.active

        response = client.post(
            '/categories/deactivate/{}'.format(
                response['data']['id']),
            headers={
                "Content-Type": "application/json"
            }
        )

        deactivate_response_data = json.loads(response.data)
        assert 'data' in deactivate_response_data
        assert 'message' in deactivate_response_data
        assert deactivate_response_data['message'] == \
               Status.successfully_processed().message
        assert deactivate_response_data['data']['state'] == 'inactive'

    @pytest.mark.run(order=6)
    def test_category_activate(self, client):
        from src import db, Category

        response = json.loads(self.create_category.data)

        x = db.session.query(Category).filter(
            Category.name == response['data']['name']).first()
        x.status = Category.STATUSES.active
        x.state = Category.STATES.inactive

        response = client.post(
            '/categories/activate/{}'.format(
                response['data']['id']),
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

    @pytest.mark.run(order=7)
    def test_category_pagination(self, client):
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
            '/category/paginate',
            json=json_data,
            headers={
                "Content-Type": "application/json"
            },
        )

        post_paginate_data = json.loads(response.data)
        assert 'data' in post_paginate_data
        assert post_paginate_data['data']['total'] > 0
        assert response.status_code == 200
