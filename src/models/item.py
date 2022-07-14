import enum
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import or_
from sqlalchemy import orm
from sqlalchemy.dialects.postgresql import UUID

from src import db
from src.models.common import BaseModelMixin, ModelsMixin


class ItemQuery(BaseModelMixin, db.Query):

    def get_one_by_id(self, _id):
        try:
            return self.filter(
                Item.id == _id,
                Item.status == Item.STATUSES.active
            ).first()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_items(filter_data, start, length):
        try:
            return db.session.query(
                Item
            ).filter(
                filter_data,
                Item.status == Item.STATUSES.active
            ).order_by('created_at').paginate(
                page=start, per_page=length, error_out=False, max_per_page=50
            )
        except Exception as e:
            db.session.rollback()
            raise e



    def autocomplete(self, search):
        try:
            return self.filter(
                Item.status == Item.STATUSES.active,
                or_(
                    Item.name.ilike('%' + search + '%')
                )
            ).all() is not None
        except Exception as e:
            db.session.rollback()
            raise e


class ItemState(enum.Enum):
    active = 'active'
    inactive = 'inactive'


class ItemStatus(enum.Enum):
    active = 1
    inactive = 0


class Item(BaseModelMixin, ModelsMixin, db.Model):
    __tablename__ = 'items'
    query_class = ItemQuery

    STATUSES = ItemStatus
    STATES = ItemState

    id = sa.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    name = sa.Column(sa.String(length=255), nullable=False)
    description = sa.Column(sa.Text(), nullable=False)
    price = sa.Column(sa.Float())
    state = sa.Column(
        sa.Enum(
            ItemState,
            name="ck_items_states",
            native_enum=False,
            create_constraint=True,
            length=255,
            validate_strings=True,
        ),
        nullable=False,
        default=ItemState.active,
        server_default=ItemState.active.name
    )
    status = sa.Column(
        sa.Enum(
            ItemStatus,
            name="ck_items_status",
            native_enum=False,
            create_constraint=True,
            length=255,
            validate_strings=True,
        ),
        nullable=False,
        default=ItemStatus.active,
        server_default=ItemStatus.active.name
    )

    subcategory_id = db.Column(UUID(as_uuid=True),
                               db.ForeignKey('subcategories.id',
                                             ondelete="RESTRICT"),
                               nullable=False,
                               index=True)

    category_id = db.Column(UUID(as_uuid=True),
                            db.ForeignKey('categories.id', ondelete="RESTRICT"),
                            nullable=False,
                            index=True)

    condition_id = db.Column(UUID(as_uuid=True),
                             db.ForeignKey('listitems.id', ondelete="RESTRICT"),
                             nullable=False,
                             index=True)

    subcategory = orm.relationship("Subcategory", back_populates="item",
                                   uselist=False)

    category = orm.relationship("Category", back_populates="item",
                                uselist=False)

    gallery = orm.relationship("Gallery", back_populates="item")

    condition = orm.relationship("ListItem", back_populates="items",
                                 uselist=False)
