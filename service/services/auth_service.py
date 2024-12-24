
from datetime import timedelta
from api.dto.dto import LoginResponse, ResetPasswordRequest, SignUpRequest, LoginRequest, SignUpResponse
from api.exception.errors import ServiceException, ValidationException
from repository.insurance.cache.cache import CacheService
from repository.insurance.model.insurance import Role, User
from repository.insurance.service.user_repo_service import UserRepoService
from service.utils.message_utils import MessageUtils
from service.utils.numerical_utils import NumericalUtils
from service.utils.response_util import ResponseUtils
from redis import Redis
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app_secrets.service.jwt_service import create_access_token
from service.utils.validation_utils import ValidationUtils
from motor.motor_asyncio import AsyncIOMotorDatabase

bcryptContext = CryptContext(schemes=['bcrypt'])


class AuthService:


    def sign_up(request: SignUpRequest, db : Session, mongo_db : AsyncIOMotorDatabase):
        if UserRepoService.fetch_by_email(request.email, db) is not None:
            raise ValidationException(MessageUtils.entity_already_exists('User', 'email', request.email))

        ValidationUtils.isTrue(request.password == request.confirm_password, MessageUtils.password_confirm_password_should_match())

        try:
            UserRepoService.insert(User(email = request.email, firstname = request.firstname, lastname = request.lastname, password = bcryptContext.hash(request.password), role = Role.ROLE_ADMIN), db)
        except Exception as e:
            raise ServiceException(errorMessage = str(e))

        access_token = create_access_token(username=request.email, expires_delta=timedelta(1), role = Role.ROLE_ADMIN.name)
        refresh_token = create_access_token(username=request.email, expires_delta=timedelta(7), role = Role.ROLE_ADMIN.name, refresh=True)

        return ResponseUtils.wrap(SignUpResponse(message= MessageUtils.signup_success_message(), access_token = access_token, refresh_token = refresh_token))

    def sign_in(request : LoginRequest, db : Session, mongo_db : AsyncIOMotorDatabase):
        user = UserRepoService.validate_and_get_by_email(request.email, db)

        ValidationUtils.isTrue(bcryptContext.verify(request.password, user.password), MessageUtils.invalid_password())
        
        access_token = create_access_token(username=request.email, expires_delta=timedelta(1), role = user.role.name)
        refresh_token = create_access_token(username=request.email, expires_delta=timedelta(7), role = user.role.name, refresh=True)

        return ResponseUtils.wrap(LoginResponse(message = MessageUtils.login_success_message(), access_token = access_token, refresh_token = refresh_token))
    

    def forget_password(email, db : Session, cache : Redis, mongo_db : AsyncIOMotorDatabase):
        user = UserRepoService.validate_and_get_by_email(email, db)

        if CacheService.has('RESET_PASSWORD_' + email, cache):
           raise ValidationException('OTP has already sent to the registered email')

        CacheService.put('RESET_PASSWORD_' + email, NumericalUtils.get_numerical_string(4), cache) 

        return ResponseUtils.wrap('Password reset otp has been sent to the mail')
    
    def reset_password(request : ResetPasswordRequest, db : Session, cache : Redis, mongo_db : AsyncIOMotorDatabase):
        user = UserRepoService.validate_and_get_by_email(request.email, db)
       
        if not CacheService.has('RESET_PASSWORD_' + request.email, cache):
            raise ValidationException('OTP has been expired or not generated')

        ValidationUtils.isTrue(request.password == request.confirm_password, MessageUtils.password_confirm_password_should_match()) 
        ValidationUtils.isTrue(not bcryptContext.verify(request.password, user.password), 'New Password should not be same as old password')
        ValidationUtils.isTrue(request.otp == CacheService.get('RESET_PASSWORD_' + request.email, cache), 'Invalid OTP Digits')
        user.password = bcryptContext.hash(request.password)

        UserRepoService.update(user, db)

        CacheService.delete('RESET_PASSWORD_' + request.email, cache)

        return ResponseUtils.wrap('Password is reset successfully')