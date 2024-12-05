from typing import Callable
from fastapi import Request
from fastapi.responses import JSONResponse
from api.exception.errors import ServiceException

import secrets

def create_exception_handler() -> Callable[[Request, ServiceException], JSONResponse]:

    def exception_handler(_: Request, exc: ServiceException) -> JSONResponse:
        return JSONResponse(status_code = exc.status_code , content = {'status_message' : exc.status_message,  'status_code': exc.status_code, 'exception' : exc.error_message, 'exception_id' : secrets.token_hex(16)})

    return exception_handler