class NotFoundException(Exception):
    msg = 'Not found'

    def __init__(self,msg):
        self.msg = msg;


class DatabaseValidationException(Exception):
    msg = 'Database validation error'

    def __init__(self,msg):
        self.msg = msg;


class NoJsonException(Exception):
    msg = 'No JSON found'
