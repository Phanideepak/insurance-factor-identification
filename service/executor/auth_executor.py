

from api.dto.dto import ResetPasswordRequest, SignUpRequest, LoginRequest
from service.services.auth_service import AuthService
from service.utils.validation_utils import ValidationUtils
from sqlalchemy.orm import Session
from redis import Redis
from motor.motor_asyncio import AsyncIOMotorDatabase


class AuthExecutor:
    def signup(request : SignUpRequest, db : Session, mongo_db : AsyncIOMotorDatabase):
        ValidationUtils.isEmpty(request.firstname, 'firstname')
        request.firstname = request.firstname.strip()

        ValidationUtils.isEmpty(request.lastname, 'lastname')
        request.lastname = request.lastname.strip()

        ValidationUtils.isEmpty(request.email, 'email')
        request.email = request.email.strip()

        ValidationUtils.isEmpty(request.password, 'password')
        request.password = request.password.strip()

        ValidationUtils.isEmpty(request.confirm_password, 'confirm_password')
        request.confirm_password = request.confirm_password.strip()

        return AuthService.sign_up(request, db, mongo_db)


    def signin(request : LoginRequest, db : Session, mongo_db : AsyncIOMotorDatabase):
        ValidationUtils.isEmpty(request.email, 'email')
        request.email = request.email.strip()

        ValidationUtils.isEmpty(request.password, 'password')
        request.password = request.password.strip()

        return AuthService.sign_in(request, db, mongo_db)

    def forget_password(email, db : Session, cache : Redis, mongo_db : AsyncIOMotorDatabase):
        ValidationUtils.isEmpty(email, 'email')
        email = email.strip() 

        return AuthService.forget_password(email, db, cache, mongo_db)


    def reset_password(request : ResetPasswordRequest, db : Session, cache : Redis, mongo_db : AsyncIOMotorDatabase):
        ValidationUtils.isEmpty(request.email, 'email')
        request.email = request.email.strip()

        ValidationUtils.isEmpty(request.password, 'password')
        request.password = request.password.strip()

        ValidationUtils.isEmpty(request.confirm_password, 'confirm_password')
        request.confirm_password = request.confirm_password.strip() 

        ValidationUtils.isEmpty(request.otp, 'otp')
        request.otp = request.otp.strip()

        return AuthService.reset_password(request, db, cache, mongo_db)