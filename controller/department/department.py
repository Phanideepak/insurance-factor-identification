from api.dto.dto import AddDepartmentBody, UpdateDepartmentBody
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response
from service.executor.dept_executor import DeptExecutor
from config import database, redis
from app_secrets.service.dependencies import AccessTokenBearer, RoleChecker
from redis import Redis

router = APIRouter(prefix= '/dept',tags= ['Department'])

get_db = database.get_db
get_cache = redis.get_redis
access_token_bearer = AccessTokenBearer()




# API End points

@router.post('', summary= 'Create Department', dependencies=[Depends(RoleChecker(['ROLE_ADMIN']))])
def create(request : AddDepartmentBody,  resp : Response, db : Session = Depends(get_db), tokendetails: dict = Depends(access_token_bearer)):
    responseBody = DeptExecutor.add(request, tokendetails['sub'], db)
    resp.status_code = responseBody.status_code
    return responseBody.dict(exclude_none= True)

@router.put('', summary= 'Edit Department', dependencies=[Depends(RoleChecker(['ROLE_ADMIN']))])
def update(request : UpdateDepartmentBody,  resp : Response, db : Session = Depends(get_db), tokendetails: dict = Depends(access_token_bearer)):
    responseBody = DeptExecutor.update(request, db)
    resp.status_code = responseBody.status_code
    return responseBody.dict(exclude_none= True)

@router.get('', summary= 'Get Department by id', dependencies=[Depends(RoleChecker(['ROLE_ADMIN']))])
def getById(id : int,  resp : Response, db : Session = Depends(get_db), tokendetails: dict = Depends(access_token_bearer)):
    responseBody = DeptExecutor.getById(id, db)
    resp.status_code = responseBody.status_code
    return responseBody.dict(exclude_none= True)

@router.delete('', summary= 'Delete Department by id', dependencies=[Depends(RoleChecker(['ROLE_ADMIN']))] )
def deleteById(id : int,  resp : Response, db : Session = Depends(get_db), tokendetails: dict = Depends(access_token_bearer)):
    responseBody = DeptExecutor.deleteById(id, tokendetails['sub'], db)
    resp.status_code = responseBody.status_code
    return responseBody.dict(exclude_none= True)

@router.patch('/restore', summary= 'Restore Department by id', dependencies=[Depends(RoleChecker(['ROLE_ADMIN']))])
def restoreById(id : int,  resp : Response, db : Session = Depends(get_db), tokendetails: dict = Depends(access_token_bearer)):
    responseBody = DeptExecutor.restoreById(id, db)
    resp.status_code = responseBody.status_code
    return responseBody.dict(exclude_none= True)

@router.patch('/approve', summary= 'Approve Department by id', dependencies=[Depends(RoleChecker(['ROLE_ADMIN']))])
def restoreById(id : int,  resp : Response, db : Session = Depends(get_db), tokendetails: dict = Depends(access_token_bearer)):
    responseBody = DeptExecutor.approveById(id, tokendetails['sub'], db)
    resp.status_code = responseBody.status_code
    return responseBody.dict(exclude_none= True)


@router.get('/all', summary= 'Get all departments', dependencies=[Depends(RoleChecker(['ROLE_ADMIN']))])
def getAll(resp : Response, db : Session = Depends(get_db), _: dict = Depends(access_token_bearer), cache  : Redis = Depends(get_cache)):
    responseBody = DeptExecutor.getAll(db, cache)
    resp.status_code = responseBody.status_code
    return responseBody.dict(exclude_none= True)