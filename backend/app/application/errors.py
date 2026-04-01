class ApplicationError(Exception):
    pass


class ValidationError(ApplicationError):
    pass


class UnsupportedTokenTypeError(ApplicationError):
    pass


class SlugGenerationError(ApplicationError):
    pass