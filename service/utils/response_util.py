from api.dto.dto import WrappedResponse
import secrets

class ResponseUtils:
    def wrap(data = None):
        return WrappedResponse(data = data)