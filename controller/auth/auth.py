from fastapi import APIRouter, Depends, Response
from redis import Redis
from api.dto.dto import LoginRequest, ResetPasswordRequest, SignUpRequest
from config import database, redis, nosql_db
from service.executor.auth_executor import AuthExecutor
from sqlalchemy.orm import Session
from motor.motor_asyncio import AsyncIOMotorDatabase


class AuthController:
    router = APIRouter(prefix='/auth', tags=['Auth API'])
    get_db = database.get_db
    get_mongo = nosql_db.get_db
    get_cache = redis.get_redis

    @router.post('/signup', summary='Signup API')    
    def signup(request : SignUpRequest, resp : Response, db : Session = Depends(get_db), mongo_db : AsyncIOMotorDatabase = Depends(get_mongo)):
        responseBody = AuthExecutor.signup(request, db, mongo_db)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True)
    
    @router.post('/login', summary= 'Login API')
    def signin(request : LoginRequest, resp : Response, db : Session = Depends(get_db), mongo_db : AsyncIOMotorDatabase = Depends(get_mongo)):
        responseBody = AuthExecutor.signin(request, db, mongo_db)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True)
    
    @router.patch('/forget', summary= 'Forget Password API')
    def forget(email , resp : Response, db : Session = Depends(get_db), cache  : Redis = Depends(get_cache), mongo_db : AsyncIOMotorDatabase = Depends(get_mongo)):
        responseBody = AuthExecutor.forget_password(email, db, cache, mongo_db)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True)
    
    @router.post('/reset', summary= 'Reset Password API')
    def reset(request : ResetPasswordRequest, resp : Response, db : Session = Depends(get_db), cache  : Redis = Depends(get_cache), mongo_db : AsyncIOMotorDatabase = Depends(get_mongo)):
        responseBody = AuthExecutor.reset_password(request, db, cache, mongo_db)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True)

