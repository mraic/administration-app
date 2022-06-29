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

    