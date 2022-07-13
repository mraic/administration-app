from src import ListItem


class ListItemService:

    def __init__(self, listitem=ListItem()):
        self.listitem=listitem

    @classmethod
    def get_one(cls, _id):
        return cls(listitem=ListItem.query.get_one(_id=_id))