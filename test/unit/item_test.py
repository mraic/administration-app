import copy
from types import SimpleNamespace

import pytest

from src import AppLogException, Item
from src.domain import ItemService
from src.general import Status


@pytest.mark.usefixtures("dummy_item")
class TestItemServices:

    def test_create_item(self, db, mocker):
        item_domain = ItemService(item=self.dummy_item)

        item_service = item_domain.create()

        assert item_service.message == Status.successfully_processed().message

    def test_alter_item(self, db, mocker):
        mock_item_get_one = mocker.patch(
            "src.domain.item_service.ItemService."
            "get_one_by_id", autospec=True
        )

        mock_item_get_one.return_value = ItemService(item=self.dummy_item)

        item_domain = ItemService(item=self.dummy_item)
        item_status = item_domain.alter()

        assert item_status.message == Status.successfully_processed().message

    def test_alter_item_no_exists(self, db, mocker):
        mock_item_get_one = mocker.patch(
            "src.domain.item_service.ItemService."
            "get_one_by_id", autospec=True
        )

        mock_item_get_one.return_value = ItemService(item=None)

        item_domain = ItemService(item=self.dummy_item)

        with pytest.raises(AppLogException) as ape:
            item_domain.alter()

        assert ape.value.status.message == Status.item_does_not_exists().message

    def test_alter_item_is_not_activated(self, db, mocker):
        mock_item_get_one = mocker.patch(
            "src.domain.item_service.ItemService."
            "get_one_by_id", autospec=True
        )

        data = copy.deepcopy(self.dummy_item)
        data.status = Item.STATUSES.inactive

        mock_item_get_one.return_value = ItemService(item=data)

        item_domain = ItemService(item=self.dummy_item)

        with pytest.raises(AppLogException) as ape:
            item_domain.alter()

        assert ape.value.status.message == \
               Status.item_is_not_activated().message

    def test_delete_item(self, db, mocker):
        mock_item_get_one = mocker.patch(
            "src.domain.item_service.ItemService."
            "get_one_by_id", autospec=True
        )

        mock_item_get_one.return_value = ItemService(item=self.dummy_item)

        item_domain = ItemService(item=self.dummy_item)

        item_service = item_domain.delete()

        assert item_service.message == Status.successfully_processed().message

    def test_delete_not_exists(self, db, mocker):
        mock_item_get_one = mocker.patch(
            "src.domain.item_service.ItemService."
            "get_one_by_id", autospec=True
        )

        mock_item_get_one.return_value = ItemService(item=None)

        item_domain = ItemService(item=self.dummy_item)

        with pytest.raises(AppLogException) as ape:
            item_domain.delete()

        assert ape.value.status.message == Status.item_does_not_exists().message

    def test_delete_item_not_activated(self, db, mocker):
        mock_item_get_one = mocker.patch(
            "src.domain.item_service.ItemService."
            "get_one_by_id", autospec=True
        )

        data = copy.deepcopy(self.dummy_item)
        data.status = Item.STATUSES.inactive

        mock_item_get_one.return_value = ItemService(item=data)

        item_domain = ItemService(item=self.dummy_item)

        with pytest.raises(AppLogException) as ape:
            item_domain.delete()

        assert ape.value.status.message == Status.item_is_not_activated().message

    def test_activate_item(self, db, mocker):
        mock_item_get_one = mocker.patch(
            "src.domain.item_service.ItemService."
            "get_one_by_id", autospec=True
        )

        data = copy.deepcopy(self.dummy_item)
        data.state = Item.STATES.inactive
        data.status = Item.STATUSES.active

        mock_item_get_one.return_value = ItemService(item=data)

        item_domain = ItemService(item=self.dummy_item)

        item_service = item_domain.activate(_id=data.id)

        assert item_service.message == Status.successfully_processed().message

    def test_activate_item_not_exists(self, db, mocker):
        mock_item_get_one = mocker.patch(
            "src.domain.item_service.ItemService."
            "get_one_by_id", autospec=True
        )

        mock_item_get_one.return_value = ItemService(item=None)

        item_domain = ItemService(item=self.dummy_item)

        with pytest.raises(AppLogException) as ape:
            item_domain.activate(_id=None)

        assert ape.value.status.message == Status.item_does_not_exists().message

    def test_activate_item_inactive(self, db, mocker):
        mock_item_get_one = mocker.patch(
            "src.domain.item_service.ItemService."
            "get_one_by_id", autospec=True
        )

        data = copy.deepcopy(self.dummy_item)
        data.status = Item.STATUSES.inactive

        mock_item_get_one.return_value = ItemService(item=data)

        item_domain = ItemService(item=self.dummy_item)

        with pytest.raises(AppLogException) as ape:
            item_domain.activate(_id=data.id)

        assert ape.value.status.message == Status.item_is_not_activated().message

    def test_activate_item_activated(self, db, mocker):
        mock_item_get_one = mocker.patch(
            "src.domain.item_service.ItemService."
            "get_one_by_id", autospec=True
        )

        data = copy.deepcopy(self.dummy_item)
        data.status = Item.STATUSES.active
        data.state = Item.STATES.active

        mock_item_get_one.return_value = ItemService(item=data)

        item_domain = ItemService(item=self.dummy_item)

        with pytest.raises(AppLogException) as ape:
            item_domain.activate(_id=data.id)

        assert ape.value.status.message == \
               Status.item_already_activated().message

    def test_deactivate_item(self, db, mocker):
        mock_item_get_one = mocker.patch(
            "src.domain.item_service.ItemService."
            "get_one_by_id", autospec=True
        )

        data = copy.deepcopy(self.dummy_item)
        data.status = Item.STATUSES.active

        mock_item_get_one.return_value = ItemService(item=data)

        item_domain = ItemService(item=self.dummy_item)

        item_service = item_domain.deactivate(_id=data.id)

        assert item_service.message == Status.successfully_processed().message

    def test_deactivate_item_not_exists(self, db, mocker):
        mock_item_get_one = mocker.patch(
            "src.domain.item_service.ItemService."
            "get_one_by_id", autospec=True
        )

        mock_item_get_one.return_value = ItemService(item=None)

        item_domain = ItemService(item=self.dummy_item)

        with pytest.raises(AppLogException) as ape:
            item_domain.deactivate(_id=None)

        assert ape.value.status.message == Status.item_does_not_exists().message

    def test_activate_item_not_activated(self, db, mocker):
        mock_item_get_one = mocker.patch(
            "src.domain.item_service.ItemService."
            "get_one_by_id", autospec=True
        )

        data = copy.deepcopy(self.dummy_item)
        data.status = Item.STATUSES.inactive

        mock_item_get_one.return_value = ItemService(item=data)

        item_domain = ItemService(item=self.dummy_item)

        with pytest.raises(AppLogException) as ape:
            item_domain.activate(_id=data.id)

        assert ape.value.status.message == \
               Status.item_is_not_activated().message

    def test_item_paginate(self, db, mocker):
        mock_get_all_items = mocker.patch(
            "src.models.item.ItemQuery."
            "get_all_items", autospec=True
        )

        total = 1
        data = [SimpleNamespace(Item=self.dummy_item, total=total)]

        mock_get_all_items.return_value = SimpleNamespace(
            items=data, total=total
        )

        paginate_data = dict(length=0, start=0)

        filter_data = {
            "condition_id": "",
            "date": {
                "date_from": "null",
                "date_to": "null"
            },
            "name": {
                "operator": "CONTAINS",
                "value": ""
            },
            "price": {
                "_from": 1,
                "_to": 1000
            }
        }

        data, total, status = ItemService.get_all_items(
            filter_data=filter_data, paginate_data=paginate_data
        )

        assert status.message == Status.successfully_processed().message
        assert total == total
        assert len(data) > 0

    def test_autocomplete(self, db, mocker):

        mock_item_autocomplete = mocker.patch(
            "src.models.item.ItemQuery."
            "autocomplete", autospec=True
        )

        mock_item_autocomplete.return_value = ItemService(item=self.dummy_item)

        item_domain = ItemService(item=self.dummy_item)

        data, item_status = item_domain.autocomplete(search=self.dummy_item.id)

        assert data is not None
        assert item_status.message == Status.successfully_processed().message