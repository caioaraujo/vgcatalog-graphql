class BusinessRuleException(Exception):
    pass


class GameAlreadyExistsException(BusinessRuleException):
    pass


class GameNotFoundException(BusinessRuleException):
    pass
