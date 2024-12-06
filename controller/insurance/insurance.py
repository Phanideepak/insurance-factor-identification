from fastapi import APIRouter, Depends, Response
from api.dto.dto import AddInsuranceRequest, UpdateInsuranceRequest
from config import database
from service.executor.auth_executor import AuthExecutor
from sqlalchemy.orm import Session


class InsuranceController:
    router = APIRouter(prefix='/insurance', tags=['Insurance API'])
    get_db = database.get_db

    @router.post('', summary='Add Insurance Plan API')    
    def add_insurance_plan(request : AddInsuranceRequest, resp : Response, db : Session = Depends(get_db)):
        responseBody = AuthExecutor.signup(request, db)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True)
    
    @router.put('', summary= 'Update Insurance Plan API')
    def update_insurance_plan(request : UpdateInsuranceRequest, resp : Response, db : Session = Depends(get_db)):
        responseBody = AuthExecutor.signin(request, db)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True)


    


