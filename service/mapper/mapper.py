from typing import List

from api.dto.dto import AddInsuranceRequest, InsuranceDto, LifeInsuranceDto, LifeInsuranceInput
from repository.insurance.model.insurance import InsurancePlan, LifeInsuranceDetail


class Mapper:
    def toInsurancePlan(request : AddInsuranceRequest):
        return InsurancePlan(insurance_name= request.insurance_name, insurance_type = request.insurance_type, description = request.description)

    def toLifeInsuranceDetail(insurance : InsurancePlan, detail : LifeInsuranceInput):
        return LifeInsuranceDetail(insurance_id = insurance.id, basic_sum_assured = detail.basic_sum_assured, interest = detail.interest, interest_type = detail.interest_type, duration=detail.duration, plan_code = f'{insurance.insurance_name}-{detail.duration}'.replace(' ', '_').upper())


class ResponseMapper:    
    def toLifeInsuranceDto(detail : LifeInsuranceDetail):
        return LifeInsuranceDto(id = detail.id, basic_sum_assured = detail.basic_sum_assured, duration = detail.duration, interest = detail.interest, interest_type = detail.interest_type)

    @classmethod
    def toLifeInsuranceDtos(cls, details : List[LifeInsuranceDetail]):
        return [cls.toLifeInsuranceDto(detail) for detail in details]

    @classmethod
    def toInsuranceDto(cls, insurance : InsurancePlan, detail_list : List[LifeInsuranceDetail]):
        return InsuranceDto(insurance_id = insurance.id, insurance_name = insurance.insurance_name, insurance_type = insurance.insurance_type, description = insurance.description, life_insurance_details = cls.toLifeInsuranceDtos(detail_list))