from sqlalchemy import and_

from src import Category, AppLogException
from src.general import Status, filter_data_result_with_operator
from ..views import CategorySchema


class CategoryService:

    def __init__(self, category=Category()):
        self.category = category

    def create(self):

        if CategoryService.get_one_by_name(name=self.category.name):
            raise AppLogException(Status.category_exists())

        if self.category.name == '':
            raise AppLogException(Status.category_has_no_name())

        self.category.add()
        self.category.commit_or_rollback()

        return Status.successfully_processed()

    def alter(self):

        data = CategoryService.get_one_by_id(_id=self.category.id)

        if data.category is None:
            raise AppLogException(Status.category_does_not_exists())

        if data.category.status == Category.STATUSES.inactive:
            raise AppLogException(Status.category_is_not_activated())

        data.category.name = self.category.name
        data.category.category_icon = self.category.category_icon

        data.category.update()
        data.category.commit_or_rollback()

        self.category = data.category

        return Status.successfully_processed()

    def delete(self, _id):

        data = CategoryService.get_one_by_id(_id=self.category.id)

        if data.category is None:
            raise AppLogException(Status.category_does_not_exists())

        data.category.status = Category.STATUSES.inactive

        self.category = data.category

        data.category.update()
        data.category.commit_or_rollback()

        return Status.successfully_processed()

    def activate(self, _id):

        data = CategoryService.get_one_by_id(_id=self.category.id)

        if data.category is None:
            raise AppLogException(Status.category_does_not_exists())

        if data.category.status == Category.STATUSES.inactive:
            raise AppLogException(Status.category_is_not_activated())

        if data.category.state == Category.STATES.active:
            raise AppLogException(Status.category_already_activated())

        data.category.state = Category.STATES.active

        self.category = data.category

        data.category.update()
        data.category.commit_or_rollback()

        return Status.successfully_processed()

    def deactivate(self, _id):

        data = CategoryService.get_one_by_id(_id=self.category.id)

        if data.category is None:
            raise AppLogException(Status.category_does_not_exists())

        if data.category.status == Category.STATUSES.inactive:
            raise AppLogException(Status.category_is_not_activated())

        data.category.state = Category.STATES.inactive

        self.category = data.category

        data.category.update()
        data.category.commit_or_rollback()

        return Status.successfully_processed()

    @classmethod
    def get_one_by_id(cls, _id):
        return cls(category=Category.query.get_one_by_id(_id=_id))

    @staticmethod
    def get_one_by_name(name):
        return Category.query.get_one_by_name(name=name)

    @staticmethod
    def get_all_users(filter_data, paginate_data):
        filter_main = and_()
        if filter_data is not None:
            filter_main = and_(
                filter_main,
                filter_data_result_with_operator(
                    'name', Category.name,
                    filter_data
                ))

        start = paginate_data.get('start') + 1 \
            if paginate_data is not None and paginate_data['start'] else 1

        length = paginate_data.get('length') \
            if paginate_data is not None and paginate_data['length'] else 10

        data = Category.query.get_all_users(
            filter_data=filter_main, start=start, length=length
        )

        return data.items, data.total, Status.successfully_processed()
