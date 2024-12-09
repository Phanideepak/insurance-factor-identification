from fastapi import APIRouter, Depends, Response
from api.dto.dto import CreateOrderRequest, OrderPaymentRequest
from config import database
from sqlalchemy.orm import Session
from app_secrets.service.dependencies import AccessTokenBearer, RoleChecker
from service.executor.order_executor import OrderExecutor



class OrderController:
    router = APIRouter(prefix='/order', tags=['Order API'])
    get_db = database.get_db
    access_token_bearer = AccessTokenBearer()

    @router.post('/create', summary='Create Order API', dependencies=[Depends(RoleChecker(['ROLE_AGENT']))])    
    def place_order(request : CreateOrderRequest, resp : Response, db : Session = Depends(get_db), token_details = Depends(access_token_bearer)):
        responseBody = OrderExecutor.place_order(request, token_details['sub'], db)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True)

    @router.post('/pay', summary='Pay Amount for Order API', dependencies=[Depends(RoleChecker(['ROLE_CUSTOMER']))])    
    def place_order(request : OrderPaymentRequest, resp : Response, db : Session = Depends(get_db), token_details = Depends(access_token_bearer)):
        responseBody = OrderExecutor.proceed_to_payment(request, token_details['sub'], db)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True)
    
    @router.get('', summary = 'Get Order by Id', dependencies = [Depends(RoleChecker(['ROLE_ADMIN', 'ROLE_AGENT', 'ROLE_CUSTOMER']))])
    def get_customer_by_id(order_id : int, resp : Response, db : Session = Depends(get_db), token_details = Depends(access_token_bearer)):
        responseBody = OrderExecutor.get_by_id(order_id, db)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True)
    
    @router.patch('/approve', summary = 'Approve Order', dependencies = [Depends(RoleChecker(['ROLE_ADMIN']))])
    def get_customer_by_id(order_id : int, resp : Response, db : Session = Depends(get_db), token_details = Depends(access_token_bearer)):
        responseBody = OrderExecutor.approve_order(order_id, token_details['sub'], db)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True)