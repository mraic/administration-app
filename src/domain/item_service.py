from sqlalchemy import and_

from src import Item, AppLogException
from src.domain import CategoryService
from src.general import Status, filter_data_result_with_operator


class ItemService:

    def __init__(self, item=Item()):
        self.item = item

    def create(self):

        if self.item.name == '':
            raise AppLogException(Status.item_has_no_name())

        self.item.category_id = \
            CategoryService.get_one_by_id(_id=self.item.subcategory_id)
        self.item.listitems_id = '5ad4449c-fc69-11ec-b939-0242ac120002'
        self.item.add()

        self.item.commit_or_rollback()

        return Status.successfully_processed()

    def alter(self):

        data = ItemService.get_one_by_id(_id=self.item.id)

        if data.item is None:
            raise AppLogException(Status.item_does_not_exists())

        if data.item.status == Item.STATUSES.inactive:
            raise AppLogException(Status.item_is_not_activated())

        data.item.name = self.item.name
        data.item.description = self.item.description
        data.item.price = self.item.price
        data.item.condition = self.item.condition

        self.item.update()
        self.item.commit_or_rollback()

        self.item = data.item

        return Status.successfully_processed()

    def delete(self):

        data = ItemService.get_one_by_id(_id=self.item.id)

        if data.item is None:
            raise AppLogException(Status.item_does_not_exists())

        if data.item.status == Item.STATUSES.inactive:
            raise AppLogException(Status.item_is_not_activated)

        data.item.status = Item.STATUSES.inactive

        self.item = data.item

        data.item.update()
        data.item.commit_or_rollback()

        return Status.successfully_processed()

    def activate(self, _id):

        data = ItemService.get_one_by_id(_id=self.item.id)

        if data.item is None:
            raise AppLogException(Status.item_does_not_exists())

        if data.item.status == Item.STATUSES.inactive:
            raise AppLogException(Status.item_is_not_activated())

        if data.item.state == Item.STATES.active:
            raise AppLogException(Status.item_already_activated())

        data.item.state = Item.STATES.active

        self.item = data.item

        data.item.update()
        data.item.commit_or_rollback()

        return Status.successfully_processed()

    def deactivate(self, _id):

        data = ItemService.get_one_by_id(_id=self.item.id)

        if data.item is None:
            raise AppLogException(Status.item_does_not_exists())

        if data.item.status == Item.STATUSES.inactive:
            raise AppLogException(Status.item_is_not_activated())

        data.item.state = Item.STATES.inactive

        self.item = data.item

        data.item.update()
        data.item.commit_or_rollback()

        return Status.successfully_processed()

    @classmethod
    def get_one_by_id(cls, _id):
        return cls(item=Item.query.get_one_by_id(_id=_id))

    @staticmethod
    def get_all_categories(filter_data, paginate_data):
        filter_main = and_()
        if filter_data is not None:
            filter_main = and_(
                filter_main,
                filter_data_result_with_operator(
                    'name', Item.name,
                    filter_data
                ))

        start = paginate_data.get('start') + 1 \
            if paginate_data is not None and paginate_data['start'] else 1

        length = paginate_data.get('length') \
            if paginate_data is not None and paginate_data['length'] else 10

        data = Item.query.get_all_categories(
            filter_data=filter_main, start=start, length=length
        )

        return data.items, data.total, Status.successfully_processed()

    @staticmethod
    def autocomplete(search):

        data = Item.query.autocomplete(search=search)

        return data, Status.successfully_processed().message
