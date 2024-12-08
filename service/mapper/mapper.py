from typing import List

from api.dto.dto import AddCustomerRequest, AddInsuranceRequest, CustomerDto, InsuranceDto, LifeInsuranceDto, LifeInsuranceInput
from repository.insurance.model.insurance import Customer, InsurancePlan, LifeInsuranceDetail


class Mapper:
    def toInsurancePlan(request : AddInsuranceRequest):
        return InsurancePlan(insurance_name= request.insurance_name, insurance_type = request.insurance_type, description = request.description)

    def toLifeInsuranceDetail(insurance : InsurancePlan, detail : LifeInsuranceInput):
        return LifeInsuranceDetail(insurance_id = insurance.id, basic_sum_assured = detail.basic_sum_assured, interest = detail.interest, interest_type = detail.interest_type, duration=detail.duration, plan_code = f'{insurance.insurance_name}-{detail.duration}'.replace(' ', '_').upper())

    def toCustomer(request : AddCustomerRequest):
        return Customer(firstname=request.firstname, lastname= request.lastname, healthy=request.healthy, life_style=request.life_style, occupation=request.occupation, occupation_type=request.occupation_type, city=request.city, pincode=request.pincode, lat = request.lat, lng = request.lng, first_line=request.first_line, last_line=request.last_line, land_mark=request.land_mark, email = request.email, phone = request.phone)

class ResponseMapper:   
    def toCustomerDto(customer : Customer):
        return CustomerDto(id = customer.id, firstname=customer.firstname, lastname=customer.lastname, healthy=customer.healthy.name, life_style=customer.life_style.name, occupation=customer.occupation, occupation_type=customer.occupation_type.name, city = customer.city, pincode = customer.pincode, lat = customer.lat, lng = customer.lng, first_line=customer.first_line, last_line=customer.last_line, land_mark=customer.land_mark, email=customer.email, phone = customer.email) 
    
    @classmethod
    def toCustomerDtos(cls, customers : List[Customer]):
        return [cls.toCustomerDto(customer) for customer in customers]
    
    def toLifeInsuranceDto(detail : LifeInsuranceDetail):
        return LifeInsuranceDto(id = detail.id, basic_sum_assured = detail.basic_sum_assured, duration = detail.duration, interest = detail.interest, interest_type = detail.interest_type, plan_code = detail.plan_code)

    @classmethod
    def toLifeInsuranceDtos(cls, details : List[LifeInsuranceDetail]):
        return [cls.toLifeInsuranceDto(detail) for detail in details]

    @classmethod
    def toInsuranceDto(cls, insurance : InsurancePlan, detail_list : List[LifeInsuranceDetail]):
        return InsuranceDto(insurance_id = insurance.id, insurance_name = insurance.insurance_name, insurance_type = insurance.insurance_type, description = insurance.description, life_insurance_details = cls.toLifeInsuranceDtos(detail_list))