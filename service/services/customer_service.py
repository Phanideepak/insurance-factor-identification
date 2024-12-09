
from api.dto.dto import AddCustomerRequest, UpdateCustomerRequest
from sqlalchemy.orm import Session
from api.exception.errors import NotModifiedException, ServiceException
from repository.insurance.model.insurance import User
from repository.insurance.service.customer_repo_service import CustomerRepoService
from repository.insurance.service.insurance_plan_repo_service import InsurancePlanRepoService
from repository.insurance.service.life_insurance_detail_repo_service import LifeInsuranceDetailRepoService
from repository.insurance.service.user_repo_service import UserRepoService
from service.mapper.mapper import Mapper, ResponseMapper
from service.utils.response_util import ResponseUtils
from service.utils.update_utils import UpdateUtils
from passlib.context import CryptContext

bcryptContext = CryptContext(schemes=['bcrypt'])

class CustomerService:
    def add_customer(request : AddCustomerRequest, db : Session):
        try:
            CustomerRepoService.insert(Mapper.toCustomer(request), db)
            UserRepoService.insert(User(email = request.email, firstname=request.firstname, lastname=request.lastname, password = bcryptContext.hash('customer123'), role = 'ROLE_CUSTOMER'),db)
        except Exception as e:
            raise ServiceException(errorMessage = str(e))
        return ResponseUtils.wrap('Customer added successfully')
        

    def update_customer(request : UpdateCustomerRequest, db : Session):
        is_updated = False
        is_email_changed = False
        old_credential = UserRepoService.fetch_by_email(request.email, db)

        customer = CustomerRepoService.validate_and_get_by_id(request.id, db)

        if UpdateUtils.is_different(request.firstname, customer.firstname):
            is_updated = True
            customer.firstname = request.firstname

        if UpdateUtils.is_different(request.lastname, customer.lastname):
            is_updated = True
            customer.lastname = request.lastname
        
        if UpdateUtils.is_different(request.healthy, customer.healthy.name):
            is_updated = True
            customer.healthy = request.healthy
        
        if UpdateUtils.is_different(request.life_style, customer.life_style.name):
            is_updated = True
            customer.life_style = request.life_style
        
        if UpdateUtils.is_different(request.occupation, customer.occupation):
            customer.occupation = request.occupation
            is_updated = True
        
        if UpdateUtils.is_different(request.occupation_type, customer.occupation_type.name):
            is_updated = True
            customer.occupation_type = request.occupation_type
        
        if UpdateUtils.is_different(request.city, customer.city):
            is_updated = True
            customer.city = request.city
        
        if UpdateUtils.is_different(request.pincode, customer.pincode):
            is_updated = True
            customer.pincode = request.pincode

        if UpdateUtils.is_different(request.lat, customer.lat):
            is_updated = True
            customer.lat = request.lat

        if UpdateUtils.is_different(request.lng, customer.lng):
            is_updated = True
            customer.lng = request.lng  

        if UpdateUtils.is_different(request.first_line, customer.first_line):
            is_updated = True
            customer.first_line = request.first_line
        
        if UpdateUtils.is_different(request.last_line, customer.last_line):
            is_updated = True
            customer.last_line = request.last_line

        if UpdateUtils.is_different(request.land_mark, customer.land_mark):
            is_updated = True
            customer.land_mark = request.land_mark

        if UpdateUtils.is_different(request.email, customer.email):
            is_updated = True
            is_email_changed = True
            customer.email = request.email 

        if UpdateUtils.is_different(request.phone, customer.phone):
            is_updated = True
            customer.phone = request.phone        
        
        if not is_updated:
            raise NotModifiedException()

        CustomerRepoService.update(customer, db)

        if is_email_changed and old_credential:
            UserRepoService.delete_by_id(old_credential.id)

        if UserRepoService.fetch_by_email(request.email, db) is None:
                UserRepoService.insert(User(email = request.email, firstname = request.firstname, lastname=request.lastname, password=bcryptContext.hash('customer123'), role = 'ROLE_CUSTOMER'), db)            

        return ResponseUtils.wrap('Customer updated successfully')


    @classmethod
    def get_by_id(cls, id, db : Session):
        customer = CustomerRepoService.validate_and_get_by_id(id, db)
        return ResponseUtils.wrap(ResponseMapper.toCustomerDto(customer)) 

    @classmethod
    def get_all(cls, db : Session):
        customers = CustomerRepoService.validate_and_get_all(db)
        return ResponseUtils.wrap(ResponseMapper.toCustomerDtos(customers))

    def delete_by_id(id, db : Session):
        customer = CustomerRepoService.validate_and_get_by_id(id, db)
        CustomerRepoService.delete_by_id(customer.id, db)
        return ResponseUtils.wrap('Deleted Successfully')
    
    def get_premium(insurance_detail_id, premium_type, db : Session):
        insurance_detail = LifeInsuranceDetailRepoService.validate_and_get_by_id(insurance_detail_id, db)
        insurance = InsurancePlanRepoService.validate_and_get_by_id(insurance_detail.insurance_id, db)
        premium_amount = insurance_detail.basic_sum_assured / insurance_detail.duration
  
        if premium_type == 'QUARTERLY':
           premium_amount = 3 * premium_amount 
        
        if premium_type == 'HALF_YEARLY':
            premium_amount = 6 * premium_amount
        
        if premium_type == 'ANNUAL':
            premium_amount = 12 * premium_amount

        return ResponseUtils.wrap(ResponseMapper.toInsurancePremiumDetailDto(insurance, insurance_detail, premium_type, round(premium_amount, 2)))