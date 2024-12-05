from api.dto.dto import AddEmployeeRequest, UpdateEmployeeRequest
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response
from service.executor.employee_executor import EmployeeExecutor
from config import database, redis
from app_secrets.service.dependencies import AccessTokenBearer, RoleChecker


router = APIRouter(prefix= '/emp',tags= ['Employee'])


get_db = database.get_db
get_cache = redis.get_redis
access_token_bearer = AccessTokenBearer()



@router.post('', summary= 'Onboard Employee', dependencies=[Depends(RoleChecker(['ROLE_ADMIN', 'ROLE_HR']))])
def create(request : AddEmployeeRequest,  resp : Response, db : Session = Depends(get_db), tokendetails: dict = Depends(access_token_bearer)):
    responseBody = EmployeeExecutor.add(request, tokendetails['sub'], tokendetails['role'], db)
    resp.status_code = responseBody.status_code
    return responseBody.dict(exclude_none= True)

@router.put('', summary= 'Edit Employee Details', dependencies=[Depends(RoleChecker(['ROLE_ADMIN','ROLE_HR']))])
def update(request : UpdateEmployeeRequest,  resp : Response, db : Session = Depends(get_db), tokendetails: dict = Depends(access_token_bearer)):
    responseBody = EmployeeExecutor.update(request, tokendetails['sub'], tokendetails['role'], db)
    resp.status_code = responseBody.status_code
    return responseBody.dict(exclude_none= True)

@router.get('', summary= 'Get Employee by id', dependencies=[Depends(RoleChecker(['ROLE_ADMIN','ROLE_EMPLOYEE','ROLE_HR','ROLE_FINANCE']))])
def getById(id : int,  resp : Response, db : Session = Depends(get_db), tokendetails: dict = Depends(access_token_bearer)):
    responseBody = EmployeeExecutor.getById(id, db)
    resp.status_code = responseBody.status_code
    return responseBody.dict(exclude_none= True)

@router.delete('', summary= 'Delete Employee by id', dependencies=[Depends(RoleChecker(['ROLE_ADMIN']))] )
def deleteById(id : int,  resp : Response, db : Session = Depends(get_db), tokendetails: dict = Depends(access_token_bearer)):
    responseBody = EmployeeExecutor.deleteById(id, tokendetails['sub'], db)
    resp.status_code = responseBody.status_code
    return responseBody.dict(exclude_none= True)

@router.patch('/restore', summary= 'Restore Employee', dependencies=[Depends(RoleChecker(['ROLE_HR']))])
def restoreById(id : int,  resp : Response, db : Session = Depends(get_db), tokendetails: dict = Depends(access_token_bearer)):
    responseBody = EmployeeExecutor.restoreById(id, db)
    resp.status_code = responseBody.status_code
    return responseBody.dict(exclude_none= True)

@router.patch('/approve', summary= 'Approve Employee by Id', dependencies=[Depends(RoleChecker(['ROLE_HR','ROLE_ADMIN']))])
def approveById(id : int,  resp : Response, db : Session = Depends(get_db), tokendetails: dict = Depends(access_token_bearer)):
    responseBody = EmployeeExecutor.approveById(id, tokendetails['sub'], tokendetails['role'], db)
    resp.status_code = responseBody.status_code
    return responseBody.dict(exclude_none= True)


@router.get('/all', summary= 'Get all employees', dependencies=[Depends(RoleChecker(['ROLE_ADMIN']))])
def getAll(resp : Response, db : Session = Depends(get_db), _: dict = Depends(access_token_bearer)):
    responseBody = EmployeeExecutor.getAll(db)

    resp.status_code = responseBody.status_code
    return responseBody.dict(exclude_none= True)