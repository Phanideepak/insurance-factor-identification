from fastapi import APIRouter, Depends, Response
from api.dto.dto import AddInsuranceRequest, UpdateInsuranceRequest
from config import database
from sqlalchemy.orm import Session
from app_secrets.service.dependencies import AccessTokenBearer, RoleChecker
from service.executor.insurance_executor import InsuranceExecutor


class InsuranceController:
    router = APIRouter(prefix='/insurance', tags=['Insurance API'])
    get_db = database.get_db
    access_token_bearer = AccessTokenBearer()

    @router.post('', summary='Add Insurance Plan API', dependencies=[Depends(RoleChecker(['ROLE_ADMIN']))])    
    def add_insurance_plan(request : AddInsuranceRequest, resp : Response, db : Session = Depends(get_db), token_details = Depends(access_token_bearer)):
        responseBody = InsuranceExecutor.add_insurance_plan(request, db)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True)
    
    @router.put('', summary= 'Update Insurance Plan API', dependencies=[Depends(RoleChecker(['ROLE_ADMIN']))])
    def update_insurance_plan(request : UpdateInsuranceRequest, resp : Response, db : Session = Depends(get_db), token_details = Depends(access_token_bearer)):
        responseBody = InsuranceExecutor.update_insurance_plan(request, db)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True)

    @router.delete('', summary = 'Delete Insurance by Id', dependencies = [Depends(RoleChecker(['ROLE_ADMIN']))])
    def delete_by_id(id : int, resp : Response, db : Session = Depends(get_db), token_details = Depends(access_token_bearer)):
        responseBody = InsuranceExecutor.delete_by_id(id, db)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True)     
    
    
    @router.get('', summary = 'Get Insurance by Id', dependencies = [Depends(RoleChecker(['ROLE_ADMIN']))])
    def get_insurance_by_id(id : int, resp : Response, db : Session = Depends(get_db), token_details = Depends(access_token_bearer)):
        responseBody = InsuranceExecutor.get_by_id(id, db)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True) 

    @router.get('/all', summary = 'Get All Insurances', dependencies = [Depends(RoleChecker(['ROLE_ADMIN']))])
    def get_all_insurances(resp : Response, db : Session = Depends(get_db), token_details = Depends(access_token_bearer)):
        responseBody = InsuranceExecutor.get_all(db)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True) 

    


