import enum
from uuid import uuid4

from sqlalchemy import orm
from sqlalchemy.dialects.postgresql import UUID

from src import db
from src.models.common import BaseModelMixin, ModelsMixin
import sqlalchemy as sa

class ItemQuery(BaseModelMixin, db.Query):
    pass

class ItemState(enum.Enum):
    active='active'
    inactive='inactive'

class ItemStatus(enum.Enum):
    active = 1
    inactive=0

class Item(BaseModelMixin, ModelsMixin, db.Model):
    __tablename__ = 'items'
    query_class = ItemQuery

    id = sa.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    name = sa.Column(sa.String(length=255), nullable=False)
    description =sa.Column(sa.Text(), nullable=False)
    price = sa.Column(sa.Float())
    state = sa.Column(
        sa.Enum(
            ItemState,
            name="ck_items_states",
            native_enum = False,
            create_constraint = True,
            length=255,
            validate_strings=True,
        ),
        nullable=False,
        default=ItemState.active,
        server_default=ItemState.active.name
    )
    status = sa.Column(
        sa.Enum(
            ItemState,
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
                            index = True)


    subcategory = orm.relationship("Subcategory", back_populates="item",
                                   uselist=False)

    category = orm.relationship("Category", back_populates = "item",
                                uselist=False)

    gallery = orm.relationship("Gallery", back_populates = "item",
                                 uselist=False)