import copy
from types import SimpleNamespace

import pytest

from src import AppLogException, Category
from src.domain import CategoryService
from src.general import Status


@pytest.mark.usefixtures("dummy_category")
class TestCategoryServices:

    def test_create_category(self, db, mocker):
        mock_category_get_one = mocker.patch(
            "src.domain.category_service.CategoryService."
            "check_if_name_exists", autospec=True
        )

        mock_category_get_one.return_value = False

        category_domain = CategoryService(category=self.dummy_category)

        category_status = category_domain.create()

        assert category_status.message == \
               Status.successfully_processed().message

    def test_create_category_exists(self, db, mocker):
        mock_category_get_one = mocker.patch(
            "src.domain.category_service.CategoryService."
            "get_one_by_name", autospec=True
        )

        data = copy.deepcopy(self.dummy_category)

        mock_category_get_one.return_value = \
            CategoryService(category=data)

        category_domain = CategoryService(category=data)

        with pytest.raises(AppLogException) as ape:
            category_domain.create()

        assert ape.value.status.message == \
               Status.category_exists().message

    def test_create_no_name(self, db, mocker):
        mock_category_get_one = mocker.patch(
            "src.domain.category_service.CategoryService."
            "get_one_by_name", autospec=True
        )

        data = copy.deepcopy(self.dummy_category)
        data.name = ''

        mock_category_get_one.return_value = CategoryService(category=data)

        category_domain = CategoryService(category=data)

        with pytest.raises(AppLogException) as ape:
            category_domain.create()

        assert ape.value.status.message == Status.category_has_no_name().message

    def test_alter_category(self, db, mocker):
        mock_category_get_one_by_id = mocker.patch(
            "src.domain.category_service.CategoryService."
            "get_one_by_id", autospec=True
        )

        mock_category_get_one_by_id.return_value = \
            CategoryService(category=self.dummy_category)

        category_domain = CategoryService(category=self.dummy_category)
        category_status = category_domain.alter()

        assert category_status.message == \
               Status.successfully_processed().message

    def test_alter_category_doesnt_exists(self, db, mocker):
        mock_category_get_ony_by_id = mocker.patch(
            "src.domain.category_service.CategoryService."
            "get_one_by_id", autospec=True
        )

        mock_category_get_ony_by_id.return_value = \
            CategoryService(category=None)

        category_domain = CategoryService(category=self.dummy_category)

        with pytest.raises(AppLogException) as ape:
            category_domain.alter()

        assert ape.value.status.message == \
               Status.category_does_not_exists().message

    def test_alter_category_not_activated(self, db, mocker):
        mock_category_get_ony_by_id = mocker.patch(
            "src.domain.category_service.CategoryService."
            "get_one_by_id", autospec=True
        )

        data = copy.deepcopy(self.dummy_category)
        data.status = Category.STATUSES.inactive

        mock_category_get_ony_by_id.return_value = \
            CategoryService(category=data)

        category_domain = CategoryService(category=self.dummy_category)

        with pytest.raises(AppLogException) as ape:
            category_domain.alter()

        assert ape.value.status.message == \
               Status.category_is_not_activated().message

    def test_category_delete(self, db, mocker):
        mock_category_get_ony_by_id = mocker.patch(
            "src.domain.category_service.CategoryService."
            "get_one_by_id", autospec=True
        )

        mock_category_get_ony_by_id.return_value = \
            CategoryService(category=self.dummy_category)

        category_domain = CategoryService(category=self.dummy_category)

        category_status = category_domain.delete(_id=self.dummy_category.id)

        assert category_status.message == \
               Status.successfully_processed().message

    def test_delete_category_doesnt_exists(self, db, mocker):
        mock_category_get_ony_by_id = mocker.patch(
            "src.domain.category_service.CategoryService."
            "get_one_by_id", autospec=True
        )

        mock_category_get_ony_by_id.return_value = \
            CategoryService(category=None)

        category_domain = CategoryService(category=self.dummy_category)

        with pytest.raises(AppLogException) as ape:
            category_domain.alter()

        assert ape.value.status.message == \
               Status.category_does_not_exists().message

    def test_category_activate(self, db, mocker):
        mock_category_get_ony_by_id = mocker.patch(
            "src.domain.category_service.CategoryService."
            "get_one_by_id", autospec=True
        )

        data = copy.deepcopy(self.dummy_category)
        data.status = None

        mock_category_get_ony_by_id.return_value = \
            CategoryService(category=data)

        category_domain = CategoryService(category=self.dummy_category)

        category_status = category_domain.activate(_id=self.dummy_category.id)

        assert category_status.message == \
               Status.successfully_processed().message

    def test_category_does_not_exists(self, db, mocker):
        mock_category_get_ony_by_id = mocker.patch(
            "src.domain.category_service.CategoryService."
            "get_one_by_id", autospec=True
        )

        mock_category_get_ony_by_id.return_value = \
            CategoryService(category=None)

        category_domain = CategoryService(category=self.dummy_category)

        with pytest.raises(AppLogException) as ape:
            category_domain.activate(_id=self.dummy_category)

        assert ape.value.status.message == \
               Status.category_does_not_exists().message

    def test_category_is_not_activated(self, db, mocker):
        mock_category_get_ony_by_id = mocker.patch(
            "src.domain.category_service.CategoryService."
            "get_one_by_id", autospec=True
        )

        data = copy.deepcopy(self.dummy_category)
        data.status = Category.STATUSES.inactive

        mock_category_get_ony_by_id.return_value = \
            CategoryService(category=data)

        category_domain = CategoryService(category=self.dummy_category)

        with pytest.raises(AppLogException) as ape:
            category_domain.activate(_id=data.id)

        assert ape.value.status.message == \
               Status.category_is_not_activated().message

    def test_category_already_activated(self, db, mocker):
        mock_category_get_ony_by_id = mocker.patch(
            "src.domain.category_service.CategoryService."
            "get_one_by_id", autospec=True
        )

        data = copy.deepcopy(self.dummy_category)
        data.state = Category.STATES.active
        data.status = Category.STATES.active

        mock_category_get_ony_by_id.return_value = \
            CategoryService(category=data)

        data_ = copy.deepcopy(self.dummy_category)
        data_.state = Category.STATES.active

        category_domain = CategoryService(category=data_)

        with pytest.raises(AppLogException) as ape:
            category_domain.activate(_id=data.id)

        assert ape.value.status.message == \
               Status.category_already_activated().message

    def test_category_deactivate(self, db, mocker):
        mock_category_get_ony_by_id = mocker.patch(
            "src.domain.category_service.CategoryService."
            "get_one_by_id", autospec=True
        )

        data = copy.deepcopy(self.dummy_category)
        data.status = Category.STATUSES.active

        mock_category_get_ony_by_id.return_value = \
            CategoryService(category=data)

        category_domain = CategoryService(category=self.dummy_category)

        category_status = category_domain.deactivate(_id=self.dummy_category)

        assert category_status.message == \
               Status.successfully_processed().message

    def test_deactivate_category_not_exists(self, db, mocker):
        mock_category_get_on_by_id = mocker.patch(
            "src.domain.category_service.CategoryService."
            "get_one_by_id", autospec=True
        )

        mock_category_get_on_by_id.return_value = \
            CategoryService(category=None)

        category_domain = CategoryService(category=self.dummy_category)

        with pytest.raises(AppLogException) as ape:
            category_domain.deactivate(_id=self.dummy_category.id)

        assert ape.value.status.message == \
               Status.category_does_not_exists().message

    def test_deactivate_category_not_activated(self, db, mocker):
        mock_category_get_on_by_id = mocker.patch(
            "src.domain.category_service.CategoryService."
            "get_one_by_id", autospec=True
        )

        data = copy.deepcopy(self.dummy_category)
        data.status = Category.STATUSES.inactive

        mock_category_get_on_by_id.return_value = \
            CategoryService(category=data)

        category_domain = CategoryService(category=self.dummy_category)

        with pytest.raises(AppLogException) as ape:
            category_domain.deactivate(_id=data.id)

        assert ape.value.status.message == \
               Status.category_is_not_activated().message

    def test_category_paginate(self, db, mocker):
        mock_category = mocker.patch(
            "src.models.category.CategoryQuery."
            "get_all_categories", autospec=True
        )

        total = 1
        data = [SimpleNamespace(Category=self.dummy_category, total=total)]

        mock_category.return_value = SimpleNamespace(
            items=data, total=total
        )

        paginate_data = dict(length=0, start=0)
        filter_data = {
            "name": {
                "operator": "CONTAINS",
                "value": ""
            }
        }

        data, total, status = CategoryService.get_all_categories(
            filter_data=filter_data, paginate_data=paginate_data
        )

        assert status.message == Status.successfully_processed().message
        assert total == total
        assert len(data) > 0
