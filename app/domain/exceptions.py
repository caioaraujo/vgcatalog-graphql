class BusinessRuleException(Exception):
    message = "Business rule violation"
    code = 400

    def __init__(self, message=None, code=None):
        self.message = message or self.message
        self.code = code or self.code
        super().__init__(self.message)


class GameAlreadyExistsException(BusinessRuleException):
    message = "Game already exists for the given platform"
    code = 400


class GameNotFoundException(BusinessRuleException):
    message = "Game not found"
    code = 404
