from api.exception.errors import ServiceException, ValidationException
from repository.ems.service.user_repo_service import UserRepoService
from repository.ems.model.ems import User, Role
from api.dto.dto import SignUpRequest, SignUpResponse, LoginRequest, LoginResponse
from sqlalchemy.orm import Session
from service.utils.message_utils import MessageUtils
from service.utils.response_util import ResponseUtils
from app_secrets.service.jwt_service import create_access_token
from http import HTTPStatus
from passlib.context import CryptContext
from datetime import timedelta

from service.utils.validation_utils import ValidationUtils

bcryptContext = CryptContext(schemes=['bcrypt'])

class AuthService:
    def signup(request : SignUpRequest, db : Session):
        if UserRepoService.validateAndGetByEmail(request.email, db) is not None:
            raise ValidationException(MessageUtils.entity_already_exists('User','email', request.email))
        try:
            UserRepoService.save(User(email = request.email,firstname = request.firstname, lastname = request.lastname, password = bcryptContext.hash(request.password), role = Role.ROLE_ADMIN), db)
        except Exception as e:
            raise ServiceException(str(e))
        
        user = UserRepoService.validateAndGetByEmail(request.email, db)

        access_token = create_access_token(username = request.email, expires_delta= timedelta(days=1), role= Role.ROLE_ADMIN.name)
        refresh_token = create_access_token(username = request.email, expires_delta= timedelta(days=7), role= Role.ROLE_ADMIN.name, refresh = True)

        return ResponseUtils.wrap(SignUpResponse(message = MessageUtils.signup_success_message(), access_token = access_token, refresh_token = refresh_token))

    def signin(request : LoginRequest, db : Session):
        user = UserRepoService.validateAndGetByEmail(request.email, db)

        ValidationUtils.isTrue(bcryptContext.verify(request.password, user.password), MessageUtils.invalid_password())

        access_token = create_access_token(username = request.email, expires_delta= timedelta(days=1), role= user.role.name)
        refresh_token = create_access_token(username = request.email, expires_delta= timedelta(days=7), role= user.role.name, refresh = True)

        return ResponseUtils.wrap(LoginResponse(message = MessageUtils.login_success_message(), access_token = access_token, refresh_token = refresh_token))