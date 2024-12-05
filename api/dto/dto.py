from typing import Optional, TypeVar
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

class AddAddressRequest(BaseModel):
     first_line : str
     second_line : Optional[str] = None
     land_mark : Optional[str] = None
     phone : str 
     city : str
     pincode : str
     state : str

class UpdateAddressRequest(BaseModel):
     id : int
     first_line : str
     second_line : Optional[str] = None
     land_mark : Optional[str] = None
     phone : str 
     city : str
     pincode : str
     state : str


class AddEmployeeRequest(BaseModel):
     firstname : str
     lastname : str
     contact : str
     designation : str
     eid : str
     dept_id : int

class UpdateEmployeeRequest(BaseModel):
     firstname : str
     lastname : str
     contact : str
     designation : str
     eid : str
     dept_id : int

class AddressDto(BaseModel):
     id : int
     first_line : str
     second_line : Optional[str] = None
     land_mark : Optional[str] = None
     phone : str 
     city : str
     pincode : str
     state : str
     eid : int
     is_primary : bool



class LoginResponse(BaseModel):
     access_token : str
     refresh_token : str
     message : str

class AddDepartmentBody(BaseModel):
    name : str
    description : str

class UpdateDepartmentBody(BaseModel):
    id : int = Field(min = 1)
    name : str
    description : str

class UserDto(BaseModel):
     id : int 
     firstname : str
     lastname : str
     email : str
     role : str
class DepartmentDto(BaseModel):
     id : int
     name : str
     description : str 
     approval_status : str
     is_deleted : bool

class EmployeeDto(BaseModel):
     id : int
     eid : str
     firstname : str
     lastname : str
     contact : str
     approval_status : str
     is_deleted : bool
     approved_by : Optional[UserDto] = None
     approved_at : Optional[str] = None
     deleted_by : Optional[UserDto] = None
     deleted_at : Optional[str] = None
     created_by : UserDto
     designation : str
     office_mail : Optional[str] = None
     dept : DepartmentDto

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