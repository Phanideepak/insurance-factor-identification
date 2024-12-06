from fastapi import APIRouter, Depends, Response
from api.dto.dto import LoginRequest, SignUpRequest
from config import database
from service.executor.auth_executor import AuthExecutor
from sqlalchemy.orm import Session


class AuthController:
    router = APIRouter(prefix='/auth', tags=['Auth API'])
    get_db = database.get_db

    @router.post('/signup', summary='Signup API')    
    def signup(request : SignUpRequest, resp : Response, db : Session = Depends(get_db)):
        responseBody = AuthExecutor.signup(request, db)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True)
    
    @router.post('/login', summary= 'Login API')
    def signin(request : LoginRequest, resp : Response, db : Session = Depends(get_db)):
        responseBody = AuthExecutor.signin(request, db)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True)


    


