from fastapi import FastAPI
from controller.agent.agent import AgentController
from controller.auth.auth import AuthController 
from controller.insurance.insurance import InsuranceController
from controller.customer.customer import CustomerController
from controller.order.order import OrderController
from repository.insurance.model import insurance
from api.exception.errors import ServiceException
from api.advice.global_exception_advice import create_exception_handler
from config.database import engine



def create_app():
    app = FastAPI()
    insurance.Base.metadata.create_all(engine)
    app.include_router(AuthController.router)
    app.include_router(InsuranceController.router)
    app.include_router(CustomerController.router)
    app.include_router(AgentController.router)
    app.include_router(OrderController.router)
    app.add_exception_handler(exc_class_or_status_code =  ServiceException, handler =  create_exception_handler())
    return app