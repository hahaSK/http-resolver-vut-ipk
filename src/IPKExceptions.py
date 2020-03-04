class MethodNotAllowedException405(BaseException):
    """ Method not allowed (405) """
    pass


class BadRequestException400(BaseException):
    """ Bad Request (400) """
    pass


class InternalServerErrorException500(BaseException):
    """ Internal Server Error (500) """
    pass


class NotFoundException404(BaseException):
    """ Not Found (404) """
    pass
