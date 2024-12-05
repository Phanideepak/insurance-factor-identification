from fastapi import FastAPI
from repository.ems.model import ems
from api.exception.errors import ServiceException
from api.advice.global_exception_advice import create_exception_handler
from config.database import engine
from controller.auth import auth
from controller.user import user
from controller.department import department
from controller.address import address
from controller.employee import employee



def create_app():
    app = FastAPI()
    ems.Base.metadata.create_all(engine)
    app.include_router(auth.router)
    app.include_router(user.router)
    app.include_router(department.router)
    app.include_router(address.router)
    app.include_router(employee.router)
    app.add_exception_handler(exc_class_or_status_code =  ServiceException, handler =  create_exception_handler())
    return app