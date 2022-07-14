from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.dialects.postgresql import UUID

from src import db
from src.models.common import BaseQueryMixin, ModelsMixin, BaseModelMixin


class GalleryQuery(BaseQueryMixin, db.Query):

    def get_one(self, _id):
        try:
            return self.filter(
                Gallery.id == _id
            ).first()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_all_by_item_exclude_this(self, item_id, gallery_for_exclude):
        try:
            return self.filter(
                Gallery.items_id == item_id,
                Gallery.id != gallery_for_exclude
            ).delete()
        except Exception as e:
            db.session.rollback()
            raise e


class Gallery(BaseModelMixin, ModelsMixin, db.Model):
    __tablename__ = 'galleries'
    query_class = GalleryQuery

    id = sa.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    main_photo = sa.Column(sa.String(255), nullable=False)
    path = sa.Column(sa.String(255), nullable=False)

    items_id = db.Column(UUID(as_uuid=True),
                         db.ForeignKey('items.id',
                                       ondelete="RESTRICT"),
                         nullable=False,
                         index=True)

    item = orm.relationship("Item", back_populates="gallery",
                            uselist=False)
