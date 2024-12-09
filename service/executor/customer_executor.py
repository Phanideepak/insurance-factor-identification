
from api.dto.dto import AddCustomerRequest, UpdateCustomerRequest
from sqlalchemy.orm import Session

from service.services.customer_service import CustomerService
from service.utils.validation_utils import ValidationUtils


class CustomerExecutor:
    
    def add_customer(request : AddCustomerRequest, db : Session):
        ValidationUtils.isEmpty(request.firstname, 'firstname')
        request.firstname = request.firstname.strip()
        ValidationUtils.isEmpty(request.lastname, 'lastname')
        request.lastname = request.lastname.strip()
        ValidationUtils.isEmpty(request.healthy, 'healthy')
        request.healthy = request.healthy.strip()
        ValidationUtils.isEmpty(request.life_style, 'life_style')
        request.life_style = request.life_style.strip()
        ValidationUtils.isEmpty(request.occupation, 'occupation')
        request.occupation = request.occupation.strip()
        ValidationUtils.isEmpty(request.occupation_type, 'occupation_type')
        request.occupation_type = request.occupation_type.strip()
        ValidationUtils.isEmpty(request.city, 'city')
        request.city = request.city.strip()
        ValidationUtils.isEmpty(request.pincode, 'pincode')
        request.pincode = request.pincode.strip()
        ValidationUtils.isEmpty(request.lat, 'lat')
        request.lat = request.lat.strip()
        ValidationUtils.isEmpty(request.lng, 'lng')
        request.lng = request.lng.strip()
        ValidationUtils.isEmpty(request.first_line, 'first_line')
        if request.last_line:
            request.last_line = request.last_line.strip()
        ValidationUtils.isEmpty(request.land_mark, 'land_mark')
        request.land_mark = request.land_mark.strip()
        ValidationUtils.isEmpty(request.email, 'email')
        request.email = request.email.strip()
        ValidationUtils.isEmpty(request.phone, 'phone')
        request.phone = request.phone.strip()

        return CustomerService.add_customer(request, db)

    def update_customer(request : UpdateCustomerRequest, db : Session):
        ValidationUtils.isZero(request.id, 'customer_id')
        ValidationUtils.isEmpty(request.firstname, 'firstname')
        request.firstname = request.firstname.strip()
        ValidationUtils.isEmpty(request.lastname, 'lastname')
        request.lastname = request.lastname.strip()
        ValidationUtils.isEmpty(request.healthy, 'healthy')
        request.healthy = request.healthy.strip()
        ValidationUtils.isEmpty(request.life_style, 'life_style')
        request.life_style = request.life_style.strip()
        ValidationUtils.isEmpty(request.occupation, 'occupation')
        request.occupation = request.occupation.strip()
        ValidationUtils.isEmpty(request.occupation_type, 'occupation_type')
        request.occupation_type = request.occupation_type.strip()
        ValidationUtils.isEmpty(request.city, 'city')
        request.city = request.city.strip()
        ValidationUtils.isEmpty(request.pincode, 'pincode')
        request.pincode = request.pincode.strip()
        ValidationUtils.isEmpty(request.lat, 'lat')
        request.lat = request.lat.strip()
        ValidationUtils.isEmpty(request.lng, 'lng')
        request.lng = request.lng.strip()
        ValidationUtils.isEmpty(request.first_line, 'first_line')
        if request.last_line:
            request.last_line = request.last_line.strip()
        ValidationUtils.isEmpty(request.land_mark, 'land_mark')
        request.land_mark = request.land_mark.strip()
        ValidationUtils.isEmpty(request.email, 'email')
        request.email = request.email.strip()
        ValidationUtils.isEmpty(request.phone, 'phone')
        request.phone = request.phone.strip()
        
        return CustomerService.update_customer(request, db)

    def get_by_id(id, db : Session):
        ValidationUtils.isZero(id, 'id')
        
        return CustomerService.get_by_id(id, db)

    def get_all(db : Session):
        return CustomerService.get_all(db)

    def delete_by_id(id, db : Session):
        ValidationUtils.isZero(id, 'id')

        return CustomerService.delete_by_id(id, db)
    
    def get_premium(insurance_detail_id, premium_type, db : Session):
        ValidationUtils.isZero(insurance_detail_id, 'insurance_detail_id')
        ValidationUtils.isEmpty(premium_type, 'premium_type')
        premium_type = premium_type.strip()

        return CustomerService.get_premium(insurance_detail_id, premium_type, db)