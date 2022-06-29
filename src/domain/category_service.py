from src import Category, AppLogException
from src.general import Status
from ..views import CategorySchema


class CategoryService:

    def __init__(self, category=Category()):
        self.category = category

    def create(self):

        if CategoryService.get_one_by_name(name=self.category.name):
            raise AppLogException(Status.category_exists())

        self.category.name.strip()
        self.category.add()
        self.category.commit_or_rollback()

        return Status.successfully_processed()


    @staticmethod
    def get_one_by_name(name):
        return Category.query.get_one_by_name(name=name)