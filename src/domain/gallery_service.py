from src import Gallery, AppLogException
from src.general import Status


class GalleryService:

    def __init__(self, gallery=Gallery()):
        self.gallery = gallery

    def create(self):
        self.gallery.add()
        self.gallery.flush()

        return Status.successfully_processed()

    def alter(self):
        data = GalleryService.get_one(_id=self.gallery.id)

        if data.gallery is None:
            raise AppLogException(Status.gallery_does_not_exists())

        self.gallery = data.gallery
        self.gallery.update()
        self.gallery.commit_or_rollback()

        return Status.successfully_processed()

    @classmethod
    def get_one(cls, _id):
        return cls(gallery=Gallery.query.get_one(_id=_id))

    @staticmethod
    def delete_all_by_item_without_this(
            item_id, gallery_for_exclude):
        Gallery.query.delete_all_by_item_exclude_this(
            item_id=item_id, gallery_for_exclude=gallery_for_exclude
        )
