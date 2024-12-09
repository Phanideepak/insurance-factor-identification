
from datetime import timedelta
from api.dto.dto import LoginResponse, SignUpRequest, LoginRequest, SignUpResponse
from api.exception.errors import ServiceException, ValidationException
from repository.insurance.model.insurance import Role, User
from repository.insurance.service.user_repo_service import UserRepoService
from service.utils.message_utils import MessageUtils
from service.utils.response_util import ResponseUtils
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app_secrets.service.jwt_service import create_access_token
from service.utils.validation_utils import ValidationUtils

bcryptContext = CryptContext(schemes=['bcrypt'])


class AuthService:


    def sign_up(request: SignUpRequest, db : Session):
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

    def sign_in(request : LoginRequest, db : Session):
        user = UserRepoService.validate_and_get_by_email(request.email, db)

        ValidationUtils.isTrue(bcryptContext.verify(request.password, user.password), MessageUtils.invalid_password())
        
        access_token = create_access_token(username=request.email, expires_delta=timedelta(1), role = user.role.name)
        refresh_token = create_access_token(username=request.email, expires_delta=timedelta(7), role = user.role.name, refresh=True)

        return ResponseUtils.wrap(LoginResponse(message = MessageUtils.login_success_message(), access_token = access_token, refresh_token = refresh_token))