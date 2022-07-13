from pathlib import Path

from sqlalchemy import and_

from src import Item, AppLogException, Gallery, db
from src.domain import SubcategoryService
from src.general import Status, filter_data_result_with_operator, \
    filter_data_result_between_two_dates, filter_data_result_between_two_value, \
    import_file


class ItemService:

    def __init__(self, item=Item()):
        self.item = item

    def create(self):
        from src.domain import ListItemService

        data = SubcategoryService.get_one_by_id(_id=self.item.subcategory_id)

        if data.subcategory is None:
            raise AppLogException(Status.subcategory_doesnt_exists())

        data_condition = ListItemService.get_one(_id=self.item.condition_id)

        if data_condition.listitem is None:
            raise AppLogException(Status.condition_doesnt_exists())

        self.item.category_id = str(data.subcategory.category_id)
        self.item.add()
        self.item.flush()

        return Status.successfully_processed()

    def alter(self):

        data = ItemService.get_one_by_id(_id=self.item.id)

        if data.item is None:
            raise AppLogException(Status.item_does_not_exists())

        if data.item.status == Item.STATUSES.inactive:
            raise AppLogException(Status.item_is_not_activated())

        if not self.item.name == '':
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
            raise AppLogException(Status.item_is_not_activated())

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
    def get_all_items(filter_data, paginate_data):
        filter_main = and_()
        if filter_data is not None:
            filter_main = and_(
                filter_main,
                Item.condition_id == filter_data.get('condition_id')
                if filter_data.get('condition_id') is not None else True,
                filter_data_result_with_operator(
                    'name', Item.name, filter_data),

                filter_data_result_between_two_value('price',
                                                     '_from',
                                                     '_to',
                                                     Item.price,
                                                     filter_data),

                filter_data_result_between_two_dates('created_at',
                                                     'date_from',
                                                     'date_to',
                                                     Item.created_at,
                                                     filter_data
                                                     ),
            )

        start = paginate_data.get('start') + 1 \
            if paginate_data is not None and paginate_data['start'] else 1

        length = paginate_data.get('length') \
            if paginate_data is not None and paginate_data['length'] else 10

        data = Item.query.get_all_items(
            filter_data=filter_main, start=start, length=length
        )

        return data.items, data.total, Status.successfully_processed()

    @staticmethod
    def autocomplete(search):

        data = Item.query.autocomplete(search=search)

        return data, Status.successfully_processed()

    @staticmethod
    def create_with_gallery(params, file):

        from src.domain import GalleryService
        try:
            item_service = ItemService(
                item=Item(
                    name=params.get('name'),
                    price=params.get('price'),
                    description=params.get('description'),
                    condition_id=params.get('condition_id'),
                    subcategory_id=params.get('subcategory_id')))
            status = item_service.create()

            Path('static/items/' + str(
                item_service.item.id)).mkdir(parents=True, exist_ok=True)
            extension = file.filename.rsplit(".", 1)[1]
            new_file_name = str(item_service.item.id) + '.' + extension
            path = 'static/items/' + str(item_service.item.id) + '/'

            import_file(path=path, file=file, file_name=new_file_name)

            gallery_service = GalleryService(
                gallery=Gallery(
                    path='/' + path + new_file_name,
                    main_photo='test',
                    items_id=item_service.item.id
                ))
            gallery_service.create()

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

        return dict(message=status.message, data=item_service.item)
