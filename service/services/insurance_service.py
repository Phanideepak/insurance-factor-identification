
from api.dto.dto import AddInsuranceRequest, UpdateInsuranceRequest
from api.exception.errors import NotModifiedException, ServiceException, ValidationException
from repository.insurance.model.insurance import InsurancePlan
from repository.insurance.service.insurance_plan_repo_service import InsurancePlanRepoService
from repository.insurance.service.life_insurance_detail_repo_service import LifeInsuranceDetailRepoService
from service.mapper.mapper import Mapper, ResponseMapper
from service.utils.message_utils import MessageUtils
from service.utils.response_util import ResponseUtils
from sqlalchemy.orm import Session

from service.utils.update_utils import UpdateUtils


class InsuranceService:
    def add_insurance_plan(request: AddInsuranceRequest, db : Session):
        if InsurancePlanRepoService.fetch_by_insurance_name(request.insurance_name, db) :
            raise ValidationException(MessageUtils.entity_already_exists('Insurance', 'insurance_name', request.insurance_name))

        try:
            InsurancePlanRepoService.insert(Mapper.toInsurancePlan(request), db)

            insurance = InsurancePlanRepoService.fetch_by_insurance_name(request.insurance_name, db)

            for detail in request.life_insurance_details:
                LifeInsuranceDetailRepoService.add(Mapper.toLifeInsuranceDetail(insurance, detail), db)

        except Exception as e:
            raise ServiceException(str(e))

        return ResponseUtils.wrap('Added Successfully')

    def update_insurance_plan(request : UpdateInsuranceRequest, db : Session):
        insurance  = InsurancePlanRepoService.validate_and_get_by_id(request.insurance_id, db)
        is_updated = False 

        if UpdateUtils.is_different(request.insurance_name, insurance.insurance_name):
            is_updated = True
            insurance.insurance_name = request.insurance_name
        
        if UpdateUtils.is_different(request.insurance_type, insurance.insurance_type.name):
            is_updated = True
            insurance.insurance_type = request.insurance_type
        
        if UpdateUtils.is_different(request.description, insurance.description):
            insurance.description = request.description
            is_updated = True
        
        if is_updated:
            InsurancePlanRepoService.update(insurance, db)

        for detail in request.life_insurance_details:
            existing_detail = LifeInsuranceDetailRepoService.validate_and_get_by_id(detail.id, db)

            if UpdateUtils.is_different(detail.basic_sum_assured, existing_detail.basic_sum_assured):
                is_updated = True
                existing_detail.basic_sum_assured = detail.basic_sum_assured
            
            if UpdateUtils.is_different(detail.duration, existing_detail.duration):
                is_updated = True
                existing_detail.duration = detail.duration
            
            if UpdateUtils.is_different(detail.interest, existing_detail.interest):
                is_updated = True
                existing_detail.interest = detail.interest
            
            if UpdateUtils.is_different(detail.interest_type, existing_detail.interest_type.name):
                is_updated = True
                existing_detail.interest_type = detail.interest_type
            
            if is_updated:
                LifeInsuranceDetailRepoService.update(existing_detail, db)

        if not is_updated:
            raise NotModifiedException()

        return ResponseUtils.wrap('Updated Successfully')
    
    def __to_insurance_dto(insurance : InsurancePlan, db : Session):
        life_insurance_details = LifeInsuranceDetailRepoService.fetch_by_insurance_id(insurance.id, db)
        return ResponseMapper.toInsuranceDto(insurance, life_insurance_details)

    @classmethod 
    def get_insurance_by_id(cls, id, db : Session):
        insurance = InsurancePlanRepoService.validate_and_get_by_id(id, db)
        return ResponseUtils.wrap(cls.__to_insurance_dto(insurance, db))
    

    @classmethod
    def get_all(cls, db : Session):
        insurances = InsurancePlanRepoService.validate_and_fetch_all(db)
        return ResponseUtils.wrap([cls.__to_insurance_dto(insurance, db) for insurance in insurances])
    

    def delete_by_id(id, db : Session):
        insurance = InsurancePlanRepoService.validate_and_get_by_id(id, db)
        try:
            LifeInsuranceDetailRepoService.delete_by_insurance_id(insurance.id, db)
            InsurancePlanRepoService.delete_by_id(insurance.id, db)
        except Exception as e:
            raise ServiceException(str(e))
        return ResponseUtils.wrap('Deleted Successfully')