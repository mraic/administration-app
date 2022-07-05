import copy
from types import SimpleNamespace

import pytest

from src import AppLogException, Subcategory
from src.domain.subcategory_service import SubcategoryService
from src.general import Status


@pytest.mark.usefixtures("dummy_subcategory")
class TestSubcategoryServices:

    def test_create_subcategory(self, db, mocker):
        mock_check_subcategory = mocker.patch(
            "src.domain.subcategory_service.SubcategoryService."
            "check_if_subcategory_exists", autospec=True
        )

        mock_check_subcategory.return_value = False

        subcategory_domain = \
            SubcategoryService(subcategory=self.dummy_subcategory)

        status = subcategory_domain.create()

        assert status.message == Status.successfully_processed().message

    def test_create_empty_name(self, db, mocker):
        mock_check_subcategory = mocker.patch(
            "src.domain.subcategory_service.SubcategoryService."
            "check_if_subcategory_exists", autospec=True
        )

        mock_check_subcategory.return_value = False

        data = copy.deepcopy(self.dummy_subcategory)
        data.name = ''

        subcategory_domain = \
            SubcategoryService(subcategory=data)

        with pytest.raises(AppLogException) as ape:
            subcategory_domain.create()

        assert ape.value.status.message == \
               Status.subcategory_cant_be_blank().message

    def test_create_subcategory_exists(self, db, mocker):
        mock_check_subcategory = mocker.patch(
            "src.domain.subcategory_service.SubcategoryService."
            "check_if_subcategory_exists", autospec=True
        )

        mock_check_subcategory.return_value = \
            SubcategoryService(subcategory=self.dummy_subcategory)

        subcategory_domain = \
            SubcategoryService(subcategory=self.dummy_subcategory)

        with pytest.raises(AppLogException) as ape:
            subcategory_domain.create()

        assert ape.value.status.message == \
               Status.subcategory_exists().message

    def test_alter_subcategory(self, db, mocker):
        mock_check_subcategory = mocker.patch(
            "src.domain.subcategory_service.SubcategoryService."
            "get_one_by_id", autospec=True
        )

        data = copy.deepcopy(self.dummy_subcategory)
        data.status = Subcategory.STATUSES.active

        mock_check_subcategory.return_value = \
            SubcategoryService(subcategory=data)

        subcategory_domain = \
            SubcategoryService(subcategory=self.dummy_subcategory)

        subcategory_status = subcategory_domain.alter()

        assert subcategory_status.message == \
               Status.successfully_processed().message

    def test_alter_subcategory_not_exists(self, db, mocker):
        mock_check_subcategory = mocker.patch(
            "src.domain.subcategory_service.SubcategoryService."
            "get_one_by_id", autospec=True
        )

        mock_check_subcategory.return_value = \
            SubcategoryService(subcategory=None)

        subcategory_domain = \
            SubcategoryService(subcategory=self.dummy_subcategory)

        with pytest.raises(AppLogException) as ape:
            subcategory_domain.alter()

        assert ape.value.status.message == \
               Status.subcategory_doesnt_exists().message

    def test_alter_subcategory_not_activated(self, db, mocker):
        mock_check_subcategory = mocker.patch(
            "src.domain.subcategory_service.SubcategoryService."
            "get_one_by_id", autospec=True
        )

        data = copy.deepcopy(self.dummy_subcategory)
        data.status = Subcategory.STATUSES.inactive

        mock_check_subcategory.return_value = \
            SubcategoryService(subcategory=data)

        subcategory_domain = \
            SubcategoryService(subcategory=self.dummy_subcategory)

        with pytest.raises(AppLogException) as ape:
            subcategory_domain.alter()

        assert ape.value.status.message == \
               Status.subcategory_not_activated().message

    def test_delete_subcategory(self, db, mocker):
        mock_check_subcategory = mocker.patch(
            "src.domain.subcategory_service.SubcategoryService."
            "get_one_by_id", autospec=True
        )

        mock_check_subcategory.return_value = \
            SubcategoryService(subcategory=self.dummy_subcategory)

        subcategory_domain = \
            SubcategoryService(subcategory=self.dummy_subcategory)

        subcategory_status = \
            subcategory_domain.delete(_id=self.dummy_subcategory.id)

        assert subcategory_status.message == \
               Status.successfully_processed().message

    def test_delete_subcategory_not_exists(self, db, mocker):
        mock_check_subcategory = mocker.patch(
            "src.domain.subcategory_service.SubcategoryService."
            "get_one_by_id", autospec=True
        )

        mock_check_subcategory.return_value = \
            SubcategoryService(subcategory=None)

        subcategory_domain = \
            SubcategoryService(subcategory=self.dummy_subcategory)

        with pytest.raises(AppLogException) as ape:
            subcategory_domain.delete(_id=self.dummy_subcategory)

        assert ape.value.status.message == \
               Status.subcategory_doesnt_exists().message

    def test_delete_subcategory_deactivated(self, db, mocker):
        mock_check_subcategory = mocker.patch(
            "src.domain.subcategory_service.SubcategoryService."
            "get_one_by_id", autospec=True
        )

        data = copy.deepcopy(self.dummy_subcategory)
        data.status = Subcategory.STATUSES.inactive

        mock_check_subcategory.return_value = \
            SubcategoryService(subcategory=data)

        subcategory_domain = \
            SubcategoryService(subcategory=self.dummy_subcategory)

        with pytest.raises(AppLogException) as ape:
            subcategory_domain.delete(_id=self.dummy_subcategory)

        assert ape.value.status.message == \
               Status.subcategory_deactivated().message

    def test_activate_subcategory(self, db, mocker):
        mock_check_subcategory = mocker.patch(
            "src.domain.subcategory_service.SubcategoryService."
            "get_one_by_id", autospec=True
        )

        data = copy.deepcopy(self.dummy_subcategory)
        data.status = Subcategory.STATUSES.active

        mock_check_subcategory.return_value = \
            SubcategoryService(subcategory=data)

        subcategory_domain = \
            SubcategoryService(subcategory=self.dummy_subcategory)

        subcategory_status = \
            subcategory_domain.activate(_id=self.dummy_subcategory.id)

        assert subcategory_status.message == \
               Status.successfully_processed().message

    def test_activate_subcategory_not_exists(self, db, mocker):
        mock_check_subcategory = mocker.patch(
            "src.domain.subcategory_service.SubcategoryService."
            "get_one_by_id", autospec=True
        )

        mock_check_subcategory.return_value = \
            SubcategoryService(subcategory=None)

        subcategory_domain = \
            SubcategoryService(subcategory=self.dummy_subcategory)

        with pytest.raises(AppLogException) as ape:
            subcategory_domain.activate(_id=self.dummy_subcategory.id)

        assert ape.value.status.message == \
               Status.subcategory_doesnt_exists().message

    def test_activate_subcategory_deactivated(self, db, mocker):
        mock_check_subcategory = mocker.patch(
            "src.domain.subcategory_service.SubcategoryService."
            "get_one_by_id", autospec=True
        )

        data = copy.deepcopy(self.dummy_subcategory)
        data.status = Subcategory.STATUSES.inactive

        mock_check_subcategory.return_value = \
            SubcategoryService(subcategory=data)

        subcategory_domain = \
            SubcategoryService(subcategory=self.dummy_subcategory)

        with pytest.raises(AppLogException) as ape:
            subcategory_domain.activate(_id=self.dummy_subcategory.id)

        assert ape.value.status.message == \
            Status.subcategory_deactivated().message

    def test_activate_subcategory_activated(self, db, mocker):
        mock_check_subcategory = mocker.patch(
            "src.domain.subcategory_service.SubcategoryService."
            "get_one_by_id", autospec=True
        )

        data = copy.deepcopy(self.dummy_subcategory)
        data.status = Subcategory.STATUSES.active
        data.state = Subcategory.STATES.active

        mock_check_subcategory.return_value = \
            SubcategoryService(subcategory=data)

        subcategory_domain = \
            SubcategoryService(subcategory=self.dummy_subcategory)

        with pytest.raises(AppLogException) as ape:
            subcategory_domain.activate(_id=data.id)

        assert ape.value.status.message == \
               Status.subcategory_activated().message

    def test_deactivate(self, db, mocker):
        mock_check_subcategory = mocker.patch(
            "src.domain.subcategory_service.SubcategoryService."
            "get_one_by_id", autospec=True
        )

        data = copy.deepcopy(self.dummy_subcategory)
        data.status = Subcategory.STATUSES.active

        mock_check_subcategory.return_value = \
            SubcategoryService(subcategory=data)

        subcategory_domain = \
            SubcategoryService(subcategory=self.dummy_subcategory)

        subcategory_status = \
            subcategory_domain.deactivate(_id=self.dummy_subcategory.id)

        assert subcategory_status.message == \
               Status.successfully_processed().message

    def test_deactivate_subcategory_not_exists(self, db, mocker):
        mock_check_subcategory = mocker.patch(
            "src.domain.subcategory_service.SubcategoryService."
            "get_one_by_id", autospec=True
        )

        mock_check_subcategory.return_value = \
            SubcategoryService(subcategory=None)

        subcategory_domain = \
            SubcategoryService(subcategory=self.dummy_subcategory)

        with pytest.raises(AppLogException) as ape:
            subcategory_domain.deactivate(_id=self.dummy_subcategory.id)

        assert ape.value.status.message == \
               Status.subcategory_doesnt_exists().message

    def test_deactivate_subcategory_deactivated(self, db, mocker):
        mock_check_subcategory = mocker.patch(
            "src.domain.subcategory_service.SubcategoryService."
            "get_one_by_id", autospec=True
        )

        data = copy.deepcopy(self.dummy_subcategory)
        data.status = Subcategory.STATUSES.inactive

        mock_check_subcategory.return_value = \
            SubcategoryService(subcategory=data)

        subcategory_domain = \
            SubcategoryService(subcategory=self.dummy_subcategory)

        with pytest.raises(AppLogException) as ape:
            subcategory_domain.deactivate(_id=data.id)

        assert ape.value.status.message == \
               Status.subcategory_deactivated().message

    def test_subcategory_pagination(self, db, mocker):
        mock_category = mocker.patch(
            "src.models.subcategory.SubcategoryQuery."
            "get_all_subcategories", autospec=True
        )

        total = 1
        data = [SimpleNamespace(Subcategory=self.dummy_subcategory, total=total)]

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

        data, total, status = SubcategoryService.get_all_subcategories(
            filter_data=filter_data, paginate_data=paginate_data
        )

        assert status.message == Status.successfully_processed().message
        assert total == total
        assert len(data) > 0
