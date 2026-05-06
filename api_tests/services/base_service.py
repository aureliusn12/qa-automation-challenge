from api_tests.utils.request_helper import RequestHelper


class BaseService:
    def __init__(self, request_helper: RequestHelper):
        self.client = request_helper
