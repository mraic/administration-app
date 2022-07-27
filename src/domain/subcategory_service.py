from sqlalchemy import and_

from src import Subcategory, AppLogException
from src.domain import CategoryService
from src.general import Status, filter_data_result_with_operator


class SubcategoryService:

    def __init__(self, subcategory=Subcategory()):
        self.subcategory = subcategory

    @staticmethod
    def get(_id):

        data = SubcategoryService.get_one_by_id(_id=_id)
        if data.subcategory is not None:
            return Subcategory.query.get_one_by_id(_id=_id)
        else:
            raise AppLogException(Status.subcategory_doesnt_exists())

    def create(self):

        if SubcategoryService.check_if_subcategory_exists(
                name=self.subcategory.name, _id=self.subcategory.id):
            raise AppLogException(Status.subcategory_exists())

        self.subcategory.add()
        self.subcategory.commit_or_rollback()

        return Status.successfully_processed()

    def alter(self):

        data = SubcategoryService.get_one_by_id(_id=self.subcategory.id)

        data_subcategory = SubcategoryService.check_if_subcategory_exists(
            name=self.subcategory.name,
            _id=self.subcategory.id
        )

        if data_subcategory is True:
            raise AppLogException(Status.subcategory_exists())

        if data.subcategory is None:
            raise AppLogException(Status.subcategory_doesnt_exists())

        if data.subcategory.status == Subcategory.STATUSES.inactive:
            raise AppLogException(Status.subcategory_not_activated())

        data.subcategory.name = self.subcategory.name
        data.subcategory.subcategory_icon = self.subcategory.subcategory_icon

        data_category = \
            CategoryService.get_one_by_id(_id=self.subcategory.category_id)

        if data_category.category is not None:
            data.subcategory.category_id = self.subcategory.category_id
        else:
            raise AppLogException(Status.category_does_not_exists())

        data.subcategory.update()
        data.subcategory.commit_or_rollback()

        self.subcategory = data.subcategory

        return Status.successfully_processed()

    def delete(self):

        data = SubcategoryService.get_one_by_id(_id=self.subcategory.id)

        if data.subcategory is None:
            raise AppLogException(Status.subcategory_doesnt_exists())

        if data.subcategory.status == Subcategory.STATUSES.inactive:
            raise AppLogException(Status.subcategory_deactivated())

        data.subcategory.status = Subcategory.STATUSES.inactive

        data.subcategory.update()
        data.subcategory.commit_or_rollback()

        self.subcategory = data.subcategory

        return Status.successfully_processed()

    def activate(self):

        data = SubcategoryService.get_one_by_id(_id=self.subcategory.id)

        if data.subcategory is None:
            raise AppLogException(Status.subcategory_doesnt_exists())

        if data.subcategory.status == Subcategory.STATUSES.inactive:
            raise AppLogException(Status.subcategory_deactivated())

        if data.subcategory.state == Subcategory.STATES.active:
            raise AppLogException(Status.subcategory_activated())

        data.subcategory.state = Subcategory.STATES.active

        data.subcategory.update()
        data.subcategory.commit_or_rollback()

        self.subcategory = data.subcategory

        return Status.successfully_processed()

    def deactivate(self):

        data = SubcategoryService.get_one_by_id(_id=self.subcategory.id)

        if data.subcategory is None:
            raise AppLogException(Status.subcategory_doesnt_exists())

        if data.subcategory.status == Subcategory.STATUSES.inactive:
            raise AppLogException(Status.subcategory_deactivated())

        data.subcategory.state = Subcategory.STATES.inactive

        data.subcategory.update()
        data.subcategory.commit_or_rollback()

        self.subcategory = data.subcategory

        return Status.successfully_processed()

    @staticmethod
    def get_all_subcategories(filter_data, paginate_data):
        filter_main = and_()
        if filter_data is not None:
            filter_main = and_(
                filter_main,
                Subcategory.category_id == filter_data.get('category_id')
                if filter_data.get('category_id') is not None else True,
                filter_data_result_with_operator(
                    'name',
                    Subcategory.name,
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
    def check_if_subcategory_exists(name, _id):
        return Subcategory.query.check_if_subcategory_exists(name=name, _id=_id)
