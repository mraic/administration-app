class Status:
    def __init__(self, error_code=None, message=None):
        self.errorCode = error_code
        self.message = message

    def tuple_response(self):
        return self.errorCode, self.message

    @classmethod
    def successfully_processed(cls):
        return cls(200, 'Successfully processed')

    @classmethod
    def category_exists(cls):
        return cls(400, 'Category already exists')

    @classmethod
    def category_has_no_name(cls):
        return cls(400, "You need to provide category name")

    @classmethod
    def category_does_not_exists(cls):
        return cls(400, "Category does not exists")

    @classmethod
    def category_is_not_activated(cls):
        return cls(400, "Category is not activated")

    @classmethod
    def category_already_activated(cls):
        return cls(400, "Category is already activated")

    @classmethod
    def subcategory_exists(cls):
        return cls(400, 'Subcategory already exists')

    @classmethod
    def subcategory_cant_be_blank(cls):
        return cls(400, 'You must provide name for subcategory')

    @classmethod
    def subcategory_doesnt_exists(cls):
        return cls(400, 'Subcategory does not exists')

    @classmethod
    def subcategory_deactivated(cls):
        return cls(400, "Subcategory deleted")

    @classmethod
    def subcategory_activated(cls):
        return cls(400, "Subcategory already activated")