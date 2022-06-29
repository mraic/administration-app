import enum
from uuid import uuid4
from sqlalchemy import orm

from .common import BaseModelMixin, ModelsMixin
from .. import db
from ..models.common import BaseQueryMixin
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

class SubcategoryQuery(BaseQueryMixin, db.Query):
    pass


class SubcategoryStatus(enum.Enum):
    inactive = 0
    active = 1

class SubcategoryState(enum.Enum):
    inactive = 'inactive'
    active = 'active'


class Subcategory(BaseModelMixin, ModelsMixin, db.Model):
    __tablename__ = 'subcategories'
    query_class = SubcategoryQuery

    STATUSES = SubcategoryStatus
    STATE = SubcategoryState


    id = sa.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    name = sa.Column(sa.String(length=255), nullable=False)
    subcategory_icon = sa.Column(sa.String(length=255), nullable=False)
    state = sa.Column(
        sa.Enum(
            SubcategoryState,
            name = "ck_subcategory_states",
            native_enum=False,
            create_constraint=True,
            length=255,
            validate_strings=True,
        ),
        nullable=False,
        default=SubcategoryState.active,
        server_default=SubcategoryState.active.name
    )
    status = sa.Column(
        sa.Enum(
            SubcategoryStatus,
            name="ck_subcategory_statuses",
            native_enum=False,
            create_constraint=True,
            length=255,
            validate_strings = True,
        ),
        nullable=False,
        default=SubcategoryStatus.active,
        server_default=SubcategoryStatus.active.name
    )

    category_id = db.Column(UUID(as_uuid=True),
                            db.ForeignKey('categories.id', ondelete="RESTRICT"),
                            nullable=False,
                            index=True)

    category = orm.relationship("Category",
                                back_populates="subcategory",
                                uselist=False)

    item = orm.relationship("Item",
                             back_populates="subcategory")