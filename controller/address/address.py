from api.dto.dto import AddAddressRequest, UpdateAddressRequest
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response
from service.executor.address_executor import AddressExecutor
from config import database
from app_secrets.service.dependencies import AccessTokenBearer, RoleChecker

router = APIRouter(prefix= '/address',tags= ['Address'])


get_db = database.get_db
access_token_bearer = AccessTokenBearer()





@router.post('', summary= 'Add new Address', dependencies=[Depends(RoleChecker(['ROLE_EMPLOYEE']))])
def create(request : AddAddressRequest,  resp : Response, db : Session = Depends(get_db), tokendetails: dict = Depends(access_token_bearer)):
    responseBody = AddressExecutor.add(request, tokendetails['sub'], db)
    resp.status_code = responseBody.status_code
    return responseBody.dict(exclude_none= True)

@router.put('', summary= 'Edit Address', dependencies=[Depends(RoleChecker(['ROLE_EMPLOYEE']))])
def update(request : UpdateAddressRequest,  resp : Response, db : Session = Depends(get_db), tokendetails: dict = Depends(access_token_bearer)):
    responseBody =AddressExecutor.update(request, tokendetails['sub'], db)
    resp.status_code = responseBody.status_code
    return responseBody.dict(exclude_none= True)

@router.get('', summary= 'Get Address by id', dependencies=[Depends(RoleChecker(['ROLE_EMPLOYEE']))])
def getById(id : int,  resp : Response, db : Session = Depends(get_db), tokendetails: dict = Depends(access_token_bearer)):
    responseBody = AddressExecutor.getById(id, tokendetails['sub'], db)
    resp.status_code = responseBody.status_code
    return responseBody.dict(exclude_none= True)

@router.get('/all', summary= 'Get All Address for Employee', dependencies=[Depends(RoleChecker(['ROLE_EMPLOYEE']))])
def getAll(resp : Response, db : Session = Depends(get_db), tokendetails: dict = Depends(access_token_bearer)):
    responseBody = AddressExecutor.getAll(tokendetails['sub'], db)
    resp.status_code = responseBody.status_code
    return responseBody.dict(exclude_none= True)

@router.delete('', summary= 'Delete Address by Id', dependencies=[Depends(RoleChecker(['ROLE_EMPLOYEE']))] )
def deleteById(id : int,  resp : Response, db : Session = Depends(get_db), tokendetails: dict = Depends(access_token_bearer)):
    responseBody =AddressExecutor.deleteById(id, tokendetails['sub'], db)
    resp.status_code = responseBody.status_code
    return responseBody.dict(exclude_none= True)

@router.patch('/primary', summary= 'Set address primary', dependencies=[Depends(RoleChecker(['ROLE_EMPLOYEE']))])
def restoreById(id : int,  resp : Response, db : Session = Depends(get_db), tokendetails: dict = Depends(access_token_bearer)):
    responseBody =AddressExecutor.make_primary(id, tokendetails['sub'], db)
    resp.status_code = responseBody.status_code
    return responseBody.dict(exclude_none= True)