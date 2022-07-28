import enum
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import orm, func, and_
from sqlalchemy.dialects.postgresql import UUID

from src import db
from src.models.common import BaseModelMixin, ModelsMixin


class CategoryQuery(BaseModelMixin, db.Query):

    def get_one_by_name(self, name):
        try:
            return self.filter(
                Category.name == name).first() is not None
        except Exception as e:
            db.session.rollback()
            raise e

    def get_one_by_id(self, _id):
        try:
            return self.filter(
                Category.id == _id
            ).first()
        except Exception as e:
            db.session.rollback()
            raise e

    def check_if_name_exists(self, name):
        try:
            return self.filter(
                Category.name == name,
            ).first() is not None
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def count_subcategories():
        from src import Subcategory
        try:
            subquery = db.session.query(
                Subcategory.category_id,
                func.count(Subcategory.id).label('total')
            ).filter(
                    Subcategory.status == Subcategory.STATUSES.active
            ).group_by(
                Subcategory.category_id,
            ).subquery()

            return db.session.query(
                Category, subquery
            ).join(
                subquery,
                Category.id == subquery.c.category_id,
                isouter=True
            ).order_by(Category.created_at.desc()).all()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_categories(filter_data, start, length):
        try:
            return db.session.query(
                Category
            ).filter(
                filter_data,
                Category.status == Category.STATUSES.active
            ).paginate(
                page=start, per_page=length, error_out=False, max_per_page=50
            )
        except Exception as e:
            db.session.rollback()
            raise e

    def autocomplete(self, search):
        try:
            return self.filter(
                Category.status == Category.STATUSES.active,
                Category.name.ilike('%' + search + '%')
            ).all()
        except Exception as e:
            db.session.rollback()
            raise e

    def check_if_category_exists(self, name, _id):
        try:
            return self.filter(
                Category.name == name,
                Category.id != _id
            ).first() is not None
        except Exception as e:
            db.session.rollback()
            raise e


class CategoryStatus(enum.Enum):
    active = 1
    inactive = 0


class CategoryState(enum.Enum):
    active = 'active'
    inactive = 'inactive'


class Category(BaseModelMixin, ModelsMixin, db.Model):
    __tablename__ = "categories"
    query_class = CategoryQuery

    STATUSES = CategoryStatus
    STATES = CategoryState

    id = sa.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    name = sa.Column(sa.String(length=255), nullable=False)
    category_icon = sa.Column(sa.String(length=255), nullable=False)
    state = sa.Column(
        sa.Enum(
            CategoryState,
            name='ck_category_states',
            native_enum=False,
            create_constraint=True,
            length=255,
            validate_strings=True
        ),
        nullable=False,
        default=CategoryState.active,
        server_default=CategoryState.active.name
    )
    status = sa.Column(
        sa.Enum(
            CategoryStatus,
            name='ck_category_statuses',
            native_enum=False,
            create_constraint=True,
            length=255,
            validate_strings=True
        ),
        nullable=False,
        default=CategoryStatus.active,
        server_default=CategoryStatus.active.name
    )

    subcategory = orm.relationship("Subcategory", back_populates='category')
    item = orm.relationship("Item", back_populates='category')
