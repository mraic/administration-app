import enum
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import orm, func
from sqlalchemy.dialects.postgresql import UUID

from .common import BaseModelMixin, ModelsMixin
from .. import db
from ..models.common import BaseQueryMixin


class SubcategoryQuery(BaseQueryMixin, db.Query):

    def get_one_by_id(self, _id):
        try:
            return self.filter(
                Subcategory.id == _id
            ).first()
        except Exception as e:
            db.session.rollback()
            raise e

    def check_if_subcategory_exists(self, name, _id):
        try:
            return self.filter(
                Subcategory.name == name,
                Subcategory.id != _id
            ).first() is not None
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_subcategories(filter_data, start, length):
        try:
            return db.session.query(
                Subcategory
            ).filter(
                filter_data,
                Subcategory.status == Subcategory.STATUSES.active
            ).paginate(
                page=start, per_page=length, error_out=False, max_per_page=50
            )
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_items_per_subcategory(category_id):
        from src import Item, Category
        try:
            subquery = db.session.query(
                Item.subcategory_id,
                func.count(Item.id).label('total')
            ).having(
                func.count(Item.id).label('total') > 0
            ).group_by(
                Item.subcategory_id
            ).subquery()


            return db.session.query(
                Subcategory, subquery, Category
            ).join(
                subquery,
                Subcategory.id == subquery.c.subcategory_id,
                isouter=False
            ).join(
                Category,
                Category.id == Subcategory.category_id
            ).filter(
                Category.id == category_id
            ).all()
        except Exception as e:
            db.session.rollback()
            raise e


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
    STATES = SubcategoryState

    id = sa.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    name = sa.Column(sa.String(length=255), nullable=False)
    subcategory_icon = sa.Column(sa.String(length=255), nullable=False)
    state = sa.Column(
        sa.Enum(
            SubcategoryState,
            name="ck_subcategory_states",
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
            validate_strings=True,
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
