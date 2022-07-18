import copy

import pytest

from src import AppLogException
from src.domain import GalleryService
from src.general import Status


@pytest.mark.usefixtures("dummy_gallery")
class TestGalleryServices:

    def test_create_gallery(self, db, mocker):
        mock_items_id = mocker.patch(
            "src.domain.gallery_service.GalleryService", autospec=True
        )

        mock_items_id.return_value = GalleryService(gallery=self.dummy_gallery)

        gallery_domain = GalleryService(gallery=self.dummy_gallery)

        gallery_status = gallery_domain.create()

        assert gallery_status.message == Status.successfully_processed().message

    def test_create_gallery_item_not_exists(self, db, mocker):
        mock_items_id = mocker.patch(
            "src.domain.gallery_service.GalleryService", autospec=True
        )

        data = copy.deepcopy(self.dummy_gallery)
        data.items_id = None

        mock_items_id.return_value = GalleryService(gallery=data)

        gallery_domain = GalleryService(gallery=self.dummy_gallery)

        with pytest.raises(AppLogException) as ape:
            gallery_domain.create()

        assert ape.value.status.message == \
               Status.item_does_not_exists().message

    def test_alter_gallery(self, db, mocker):
        mock_gallery_get_one = mocker.patch(
            "src.domain.gallery_service.GalleryService.get_one", autospec=True
        )

        mock_gallery_get_one.return_value = GalleryService(
            gallery=self.dummy_gallery)

        gallery_domain = GalleryService(gallery=self.dummy_gallery)

        gallery_status = gallery_domain.alter()

        assert gallery_status.message == Status.successfully_processed().message

    def test_alter_gallery_not_exists(self, db, mocker):
        mock_gallery_get_one = mocker.patch(
            "src.domain.gallery_service.GalleryService.get_one", autospec=True
        )

        mock_gallery_get_one.return_value = GalleryService(gallery=None)

        gallery_domain = GalleryService(gallery=self.dummy_gallery)

        with pytest.raises(AppLogException) as ape:
            gallery_domain.alter()

        assert ape.value.status.message == \
               Status.gallery_does_not_exists().message
