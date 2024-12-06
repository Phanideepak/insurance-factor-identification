from typing import Optional, TypeVar, List
from pydantic import BaseModel, Field

T = TypeVar('T')

class SignUpRequest(BaseModel):
     firstname : str 
     lastname : str
     email : str 
     password: str
     confirm_password : str

class SignUpResponse(BaseModel):
     access_token : str
     refresh_token : str
     message : str

class LoginRequest(BaseModel):
     email : str 
     password: str

class LoginResponse(BaseModel):
     access_token : str
     refresh_token : str
     message : str

class LifeInsuranceInput(BaseModel):
     id : Optional[int] = None
     basic_sum_assured : int
     duration : int
     interest : float
     interest_type : str

class AddInsuranceRequest(BaseModel):
     insurance_name : str
     insurance_type : str
     description : str
     life_insurance_details : Optional[List[LifeInsuranceInput]] = None

class UpdateInsuranceRequest(BaseModel):
     insurance_id : int
     insurance_name : str
     insurance_type : str
     description : str
     life_insurance_details : Optional[List[LifeInsuranceInput]] = None

class LifeInsuranceDto(BaseModel):
     id : Optional[int] = None
     basic_sum_assured : int
     duration : int
     interest : float
     interest_type : str 

class InsuranceDto(BaseModel):
     insurance_id : int
     insurance_name : str
     insurance_type : str
     description : str
     life_insurance_details : Optional[List[LifeInsuranceDto]] = None

class UserDto(BaseModel):
     id : int 
     firstname : str
     lastname : str
     email : str
     role : str

class ResponseDto(BaseModel, object):
      status_message : str = 'Success'
      status_code : int  = 200 

class ErrorResponse(ResponseDto):
    request_id : Optional[str]  = None 
    exception_id : Optional[str] = None
    exception : Optional[str] = None

class WrappedResponse(ErrorResponse):
      data : Optional[T] = None
      def _init_(self, data = None, request_id = None, exception_id = None, exception = None, status_message = None, status_code = 0):
        super().__init__(data = data, requestId = request_id, exceptionId= exception_id, exception=exception, statusMessage = status_message, status_code = status_code)