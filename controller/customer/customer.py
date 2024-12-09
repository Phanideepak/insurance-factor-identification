from fastapi import APIRouter, Depends, Response
from api.dto.dto import AddCustomerRequest, UpdateCustomerRequest
from config import database
from sqlalchemy.orm import Session
from app_secrets.service.dependencies import AccessTokenBearer, RoleChecker
from service.executor.customer_executor import CustomerExecutor



class CustomerController:
    router = APIRouter(prefix='/customer', tags=['Customer API'])
    get_db = database.get_db
    access_token_bearer = AccessTokenBearer()

    @router.post('', summary='Add Customer API', dependencies=[Depends(RoleChecker(['ROLE_ADMIN']))])    
    def add_customer(request : AddCustomerRequest, resp : Response, db : Session = Depends(get_db), token_details = Depends(access_token_bearer)):
        responseBody = CustomerExecutor.add_customer(request, db)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True)
    
    @router.put('', summary= 'Update Customer API', dependencies=[Depends(RoleChecker(['ROLE_ADMIN']))])
    def update_customer(request : UpdateCustomerRequest, resp : Response, db : Session = Depends(get_db), token_details = Depends(access_token_bearer)):
        responseBody = CustomerExecutor.update_customer(request, db)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True)

    @router.delete('', summary = 'Delete Customer by Id', dependencies = [Depends(RoleChecker(['ROLE_ADMIN']))])
    def delete_by_id(id : int, resp : Response, db : Session = Depends(get_db), token_details = Depends(access_token_bearer)):
        responseBody = CustomerExecutor.delete_by_id(id, db)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True)     
    
    
    @router.get('', summary = 'Get Customer by Id', dependencies = [Depends(RoleChecker(['ROLE_ADMIN', 'ROLE_AGENT', 'ROLE_CUSTOMER']))])
    def get_customer_by_id(id : int, resp : Response, db : Session = Depends(get_db), token_details = Depends(access_token_bearer)):
        responseBody = CustomerExecutor.get_by_id(id, db)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True) 

    @router.get('/all', summary = 'Get All Customers', dependencies = [Depends(RoleChecker(['ROLE_ADMIN', 'ROLE_AGENT']))])
    def get_all_customers(resp : Response, db : Session = Depends(get_db), token_details = Depends(access_token_bearer)):
        responseBody = CustomerExecutor.get_all(db)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True)

    @router.get('/premium', summary = 'Get Insurance Premium', dependencies = [Depends(RoleChecker(['ROLE_CUSTOMER', 'ROLE_AGENT', 'ROLE_ADMIN']))])
    def get_premium(insurance_detail_id, premium_type, resp : Response, db : Session = Depends(get_db), token_details = Depends(access_token_bearer)):
        responseBody = CustomerExecutor.get_premium(insurance_detail_id, premium_type, db)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True)