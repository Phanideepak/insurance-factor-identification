
from api.dto.dto import AddInsuranceRequest, UpdateInsuranceRequest
from service.services.insurance_service import InsuranceService
from service.utils.validation_utils import ValidationUtils
from sqlalchemy.orm import Session


class InsuranceExecutor:
    def add_insurance_plan(request : AddInsuranceRequest, db : Session):
        ValidationUtils.isEmpty(request.insurance_name, 'insurance_name')
        request.insurance_name = request.insurance_name.strip()

        ValidationUtils.isEmpty(request.insurance_type, 'insurance_type')
        request.insurance_type = request.insurance_type.strip()

        ValidationUtils.isEmpty(request.description, 'description')
        request.description = request.description.strip()

        for detail in request.life_insurance_details:
            ValidationUtils.isZero(detail.basic_sum_assured, 'basic_sum_assured')
            ValidationUtils.isZero(detail.duration, 'duration')
            ValidationUtils.isZero(detail.interest, 'interest')
            ValidationUtils.isEmpty(detail.interest_type, 'interest_type')



        return InsuranceService.add_insurance_plan(request, db)


    def update_insurance_plan(request : UpdateInsuranceRequest, db : Session):
        ValidationUtils.isEmpty(request.insurance_name, 'insurance_name')
        request.insurance_name = request.insurance_name.strip()

        ValidationUtils.isEmpty(request.insurance_type, 'insurance_type')
        request.insurance_type = request.insurance_type.strip()

        ValidationUtils.isEmpty(request.description, 'description')
        request.description = request.description.strip()

        for detail in request.life_insurance_details:
            ValidationUtils.isZero(detail.id, 'id')
            ValidationUtils.isZero(detail.basic_sum_assured, 'basic_sum_assured')
            ValidationUtils.isZero(detail.duration, 'duration')
            ValidationUtils.isZero(detail.interest, 'interest')
            ValidationUtils.isEmpty(detail.interest_type, 'interest_type')

        return InsuranceService.update_insurance_plan(request, db)
    
    def get_by_id(id, db : Session):
        ValidationUtils.isZero(id, 'insurance_id')

        return InsuranceService.get_insurance_by_id(id, db)
    
    def get_all(db : Session):
        return InsuranceService.get_all(db)
    
    def delete_by_id(id, db : Session):
        ValidationUtils.isZero(id, 'insurance_id')

        return InsuranceService.delete_by_id(id, db)

