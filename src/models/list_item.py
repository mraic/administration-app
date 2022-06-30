import enum
from uuid import uuid4

from sqlalchemy import orm
from sqlalchemy.dialects.postgresql import UUID
from src import db
from src.models.common import BaseModelMixin, ModelsMixin

import sqlalchemy as sa


class ListItemStatus(enum.Enum):
    active = 1
    inactive = 0


class ListItem(BaseModelMixin, ModelsMixin, db.Model):

    __tablename__ = "listitems"

    id = sa.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    name = sa.Column(sa.String(length=255), nullable=False)
    description = sa.Column(sa.Text())
    status = sa.Column(
        sa.Enum(
            ListItemStatus,
            name='ck_modellist_status',
            native_enum=False,
            create_constraint=True,
            length=255,
            validate_strings=True
        ),
        nullable=False,
        default=ListItemStatus.active,
        server_default=ListItemStatus.active.name
    )

    list_id = db.Column(UUID(as_uuid=True),
                        db.ForeignKey('lists.id', ondelete="RESTRICT"),
                        nullable=False,
                        index=True
    )

    list = orm.relationship("List",
                            back_populates="list_item",
                            uselist=False)


    item = orm.relationship("Item", back_populates="list_item",
                            uselist=False)