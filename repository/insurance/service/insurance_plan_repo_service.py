from api.exception.errors import DataNotFoundException
from repository.insurance.model.insurance import InsurancePlan
from service.utils.message_utils import MessageUtils
from sqlalchemy.orm import Session


class InsurancePlanRepoService:

    def insert(insurance_plan, db : Session):
        db.add(insurance_plan)
        db.commit()
    
    def update(insurance_plan : InsurancePlan, db : Session):
        db.query(InsurancePlan).filter(InsurancePlan.id == insurance_plan.id).update({InsurancePlan.insurance_name : insurance_plan.insurance_name, InsurancePlan.insurance_type : insurance_plan.insurance_type, InsurancePlan.description : insurance_plan.description })
        db.commit()
    
    def fetch_by_id(id, db : Session):
        return db.query(InsurancePlan).filter(InsurancePlan.id == id).first()
    
    def validate_and_get_by_id(id, db : Session):
        plan = db.query(InsurancePlan).filter(InsurancePlan.id == id).first()
        if plan is None:
           raise DataNotFoundException(MessageUtils.entity_not_found('InsurancePlan', 'id', id))

        return plan 