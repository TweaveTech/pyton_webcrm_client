from requests.exceptions import JSONDecodeError

class EmptyPage(Exception):
    pass

class RequestError(Exception):
    pass