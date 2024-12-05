from typing import Any, List
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, Depends
from sqlalchemy.orm import Session
from config import database
from app_secrets.service.jwt_service import decode_token
from repository.ems.service.user_repo_service import UserRepoService
from repository.ems.model.ems import User
from api.exception.errors import TokenException, NoPermissionException

get_db = database.get_db

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error = True):
        super().__init__(auto_error = auto_error)

    # Async is mandatory
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_token(token)

        if not self.token_valid(token):
            raise TokenException('Invalid token')
        
        self.verify_token_data(token_data)

        return token_data
    
    def token_valid(self, token):
        token_data = decode_token(token)
        return token_data is not None
    
    def verify_token_data(self, token_data):
         raise TokenException("Please Override this method in child classes")
    

class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise TokenException('Access Token Required')


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise TokenException('Refresh Token Required')
        
def get_current_user(token_details : dict = Depends(AccessTokenBearer()), db : Session = Depends(get_db)):
    user_email = token_details["sub"]

    return UserRepoService.fetchByEmail(user_email, db)

class RoleChecker:
    def __init__(self, allowed_roles : List[str]):
        self.allowed_roles = allowed_roles
    
    def __call__(self, current_user : User = Depends(get_current_user)) -> Any:
        if current_user.role.name in self.allowed_roles:
            return True

        raise NoPermissionException('Insufficient Permission')