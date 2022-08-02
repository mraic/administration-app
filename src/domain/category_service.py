from sqlalchemy import and_

from src import Category, AppLogException
from src.general import Status, filter_data_result_with_operator
from src.views import CategorySchema


class CategoryService:

    def __init__(self, category=Category()):
        self.category = category

    def get(self):

        data = CategoryService.get_one_by_id(_id=self.category.id)

        if data.category is None:
            raise AppLogException(Status.category_does_not_exists())

    def create(self):

        if CategoryService.check_if_name_exists(name=self.category.name):
            raise AppLogException(Status.category_exists())

        self.category.add()
        self.category.commit_or_rollback()
        return Status.successfully_processed()

    def alter(self):
        data = CategoryService.get_one_by_id(_id=self.category.id)
        if data.category is None:
            raise AppLogException(Status.category_does_not_exists())

        if data.category.status == Category.STATUSES.inactive:
            raise AppLogException(Status.category_is_not_activated())

        if CategoryService.check_if_category_exists(
                name=self.category.name, _id=self.category.id):
            raise AppLogException(Status.category_already_exists())

        data.category.category_icon = self.category.category_icon
        data.category.name = self.category.name
        data.category.update()
        data.category.commit_or_rollback()

        self.category = data.category

        return Status.successfully_processed()

    def delete(self):

        data = CategoryService.get_one_by_id(_id=self.category.id)

        if data.category is None:
            raise AppLogException(Status.category_does_not_exists())

        if data.category.status == Category.STATUSES.inactive:
            raise AppLogException(Status.category_is_not_activated())

        data.category.status = Category.STATUSES.inactive

        data.category.update()
        data.category.commit_or_rollback()

        self.category = data.category

        return Status.successfully_processed()

    def activate(self):

        data = CategoryService.get_one_by_id(_id=self.category.id)

        if data.category is None:
            raise AppLogException(Status.category_does_not_exists())

        if data.category.status == Category.STATUSES.inactive:
            raise AppLogException(Status.category_is_not_activated())

        if data.category.state == Category.STATES.active:
            raise AppLogException(Status.category_already_activated())

        data.category.state = Category.STATES.active

        data.category.update()
        data.category.commit_or_rollback()

        self.category = data.category

        return Status.successfully_processed()

    def deactivate(self):

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
    def count_subcategories():
        data = Category.query.count_subcategories()

        list_data = []
        schema = CategorySchema()
        for i in data or []:
            current_dict = schema.dump(i.Category)
            current_dict['total'] = i.total or 0
            list_data.append(current_dict)

        return list_data, Status.successfully_processed()

    @staticmethod
    def get_one_by_id_with_check(_id):
        category_service = CategoryService.get_one_by_id(_id=_id)

        if category_service.category is None:
            raise AppLogException(Status.category_does_not_exists())

        if category_service.category.status == Category.STATUSES.inactive:
            raise AppLogException(Status.category_does_not_exists())

        return category_service, Status.successfully_processed()

    @staticmethod
    def get_one_by_name(name):
        return Category.query.get_one_by_name(name=name)

    @staticmethod
    def check_if_name_exists(name):
        return Category.query.check_if_name_exists(name=name)

    @staticmethod
    def check_if_category_exists(name, _id):
        return Category.query.check_if_category_exists(name=name, _id=_id)

    @staticmethod
    def get_all_categories(filter_data, paginate_data):
        filter_main = and_()
        if filter_data is not None:
            filter_main = and_(
                filter_main,
                filter_data_result_with_operator(
                    'name', Category.name,
                    filter_data
                )
            )

        start = paginate_data.get('start') + 1 \
            if paginate_data is not None and paginate_data['start'] else 1

        length = paginate_data.get('length') \
            if paginate_data is not None and paginate_data['length'] else 10

        data = Category.query.get_all_categories(
            filter_data=filter_main, start=start, length=length
        )

        return data.items, data.total, Status.successfully_processed()

    @staticmethod
    def autocomplete(search):

        data = Category.query.autocomplete(search=search)

        return data, Status.successfully_processed().message
