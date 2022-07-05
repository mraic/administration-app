from sqlalchemy import and_

from src import Subcategory, AppLogException
from src.domain import CategoryService
from src.general import Status, filter_data_result_with_operator


class SubcategoryService:

    def __init__(self, subcategory=Subcategory()):
        self.subcategory = subcategory

    def create(self):

        if self.subcategory.name == '':
            raise AppLogException(Status.subcategory_cant_be_blank())

        if SubcategoryService.check_if_subcategory_exists(
                name=self.subcategory.name):
            raise AppLogException(Status.subcategory_exists())

        self.subcategory.add()
        self.subcategory.commit_or_rollback()

        return Status.successfully_processed()

    def alter(self):

        data = SubcategoryService.get_one_by_id(_id=self.subcategory.id)

        if data.subcategory is None:
            raise AppLogException(Status.subcategory_doesnt_exists())

        if data.subcategory.status == Subcategory.STATUSES.inactive:
            raise AppLogException(Status.subcategory_not_activated())

        data.subcategory.name = self.subcategory.name
        data.subcategory.subcategory_icon = self.subcategory.subcategory_icon

        data_category = \
            CategoryService.get_one_by_id(_id=self.subcategory.category_id)

        if data_category is True:
            data.subcategory.category_id = self.subcategory.category_id
        else:
            raise AppLogException(Status.category_does_not_exists())

        self.subcategory = data.subcategory

        data.subcategory.update()
        data.subcategory.commit_or_rollback()

        return Status.successfully_processed()

    def delete(self, _id):

        data = SubcategoryService.get_one_by_id(_id=self.subcategory.id)

        if data.subcategory is None:
            raise AppLogException(Status.subcategory_doesnt_exists())

        if data.subcategory.status == Subcategory.STATUSES.inactive:
            raise AppLogException(Status.subcategory_deactivated())

        data.subcategory.status = Subcategory.STATUSES.inactive

        self.subcategory = data.subcategory

        data.subcategory.update()
        data.subcategory.commit_or_rollback()

        return Status.successfully_processed()

    def activate(self, _id):

        data = SubcategoryService.get_one_by_id(_id=self.subcategory.id)

        if data.subcategory is None:
            raise AppLogException(Status.subcategory_doesnt_exists())

        if data.subcategory.status == Subcategory.STATUSES.inactive:
            raise AppLogException(Status.subcategory_deactivated())

        if data.subcategory.state == Subcategory.STATES.active:
            raise AppLogException(Status.subcategory_activated())

        data.subcategory.state = Subcategory.STATES.active

        self.subcategory = data.subcategory

        data.subcategory.update()
        data.subcategory.commit_or_rollback()

        return Status.successfully_processed()

    def deactivate(self, _id):

        data = SubcategoryService.get_one_by_id(_id=self.subcategory.id)

        if data.subcategory is None:
            raise AppLogException(Status.subcategory_doesnt_exists())

        if data.subcategory.status == Subcategory.STATUSES.inactive:
            raise AppLogException(Status.subcategory_deactivated())

        data.subcategory.state = Subcategory.STATES.inactive

        self.subcategory = data.subcategory

        data.subcategory.update()
        data.subcategory.commit_or_rollback()

        return Status.successfully_processed()

    @staticmethod
    def get_all_subcategories(filter_data, paginate_data):
        filter_main = and_()
        if filter_data is not None:
            filter_main = and_(
                filter_main,
                filter_data_result_with_operator(
                    'name',
                    filter_data
                )
            )

        start = paginate_data.get('start') + 1 \
            if paginate_data is not None and paginate_data['start'] else 1

        length = paginate_data.get('length') \
            if paginate_data is not None and paginate_data['length'] else 10

        data = Subcategory.query.get_all_subcategories(
            filter_data=filter_main, start=start, length=length
        )

        return data.items, data.total, Status.successfully_processed()

    @staticmethod
    def autocomplete(search):

        data = Subcategory.query.autocomplete(search=search)

        return data, Status.successfully_processed().message

    @classmethod
    def get_one_by_id(cls, _id):
        return cls(subcategory=Subcategory.query.get_one_by_id(_id=_id))

    @staticmethod
    def check_if_subcategory_exists(name):
        return Subcategory.query.check_if_subcategory_exists(name=name)
