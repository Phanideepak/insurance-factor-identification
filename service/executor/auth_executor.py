from service.utils.validation_utils import ValidationUtils
from api.dto.dto import SignUpRequest, LoginRequest
from service.services.auth_service import AuthService
from sqlalchemy.orm import Session

class AuthExecutor:
      def signup(request : SignUpRequest, db : Session):
            ValidationUtils.isEmpty(request.firstname,'firstname')
            request.firstname = request.firstname.strip()

            ValidationUtils.isEmpty(request.lastname, 'lastname')
            request.lastname = request.lastname.strip()

            ValidationUtils.isEmpty(request.password, 'password')
            request.password = request.password.strip()

            ValidationUtils.isEmpty(request.confirm_password, 'confirm_password')
            request.confirm_password = request.confirm_password.strip()

            ValidationUtils.isTrue(request.password == request.confirm_password , 'Password and confirm password should be same')

            return AuthService.signup(request, db)
      

      def signin(request : LoginRequest, db : Session):
            ValidationUtils.isEmpty(request.password, 'password')
            request.password = request.password.strip()

            ValidationUtils.isEmpty(request.email, 'email')
            request.email = request.email.strip()

            return AuthService.signin(request, db)