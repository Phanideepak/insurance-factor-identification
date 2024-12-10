from fastapi import APIRouter, Depends, Response
from redis import Redis
from api.dto.dto import LoginRequest, ResetPasswordRequest, SignUpRequest
from config import database, redis
from service.executor.auth_executor import AuthExecutor
from sqlalchemy.orm import Session


class AuthController:
    router = APIRouter(prefix='/auth', tags=['Auth API'])
    get_db = database.get_db
    get_cache = redis.get_redis

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
    
    @router.patch('/forget', summary= 'Forget Password API')
    def forget(email , resp : Response, db : Session = Depends(get_db), cache  : Redis = Depends(get_cache)):
        responseBody = AuthExecutor.forget_password(email, db, cache)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True)
    
    @router.post('/reset', summary= 'Reset Password API')
    def reset(request : ResetPasswordRequest, resp : Response, db : Session = Depends(get_db), cache  : Redis = Depends(get_cache)):
        responseBody = AuthExecutor.reset_password(request, db, cache)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True)

