import enum
from uuid import uuid4
from src import db
from src.models.common import BaseModelMixin, ModelsMixin
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.dialects.postgresql import UUID


class CategoryQuery(BaseModelMixin, db.Query):

    def get_one_by_name(self, name):
        try:
            return self.filter(
                Category.name == name
            ).first()
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

    @staticmethod
    def get_all_users(filter_data, start, length):
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


class CategoryStatus(enum.Enum):
    inactive = 0
    active = 1


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
