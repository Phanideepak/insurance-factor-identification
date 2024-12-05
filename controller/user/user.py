from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response
from service.executor.user_executor import UserExecutor
from config import database
from app_secrets.service.dependencies import AccessTokenBearer, RoleChecker

router = APIRouter(prefix= '/user',tags= ['User'])



get_db = database.get_db
access_token_bearer = AccessTokenBearer()



# API End Point

@router.get('/all', summary= 'Get All Users', dependencies=[Depends(RoleChecker(['ROLE_ADMIN']))])
def getAll(resp : Response, db : Session = Depends(get_db), _:dict = Depends(access_token_bearer)):
    responseBody = UserExecutor.getAll(db)
    resp.status_code = responseBody.status_code
    return responseBody.dict(exclude_none= True)