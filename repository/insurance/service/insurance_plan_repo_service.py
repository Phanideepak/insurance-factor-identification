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
    
    def delete_by_id(id, db : Session):
        db.query(InsurancePlan).filter(InsurancePlan.id == id).delete()
        db.commit()
    
    def validate_and_fetch_all(db : Session):
        plans = db.query(InsurancePlan).all()

        if not plans:
            raise DataNotFoundException(MessageUtils.entities_not_found('InsurancePlans'))
        
        return plans

    def fetch_all(db : Session):
        return db.query(InsurancePlan).all()
    
    def fetch_by_id(id, db : Session):
        return db.query(InsurancePlan).filter(InsurancePlan.id == id).first()
    
    def fetch_by_insurance_name(insurance_name, db : Session):
        return db.query(InsurancePlan).filter(InsurancePlan.insurance_name == insurance_name).first()
    
    def validate_and_get_by_id(id, db : Session):
        plan = db.query(InsurancePlan).filter(InsurancePlan.id == id).first()
        if plan is None:
           raise DataNotFoundException(MessageUtils.entity_not_found('InsurancePlan', 'id', id))

        return plan

    def validate_and_get_by_insurance_name(insurance_name, db : Session):
        plan = db.query(InsurancePlan).filter(InsurancePlan.insurance_name == insurance_name).first()
        if plan is None:
           raise DataNotFoundException(MessageUtils.entity_not_found('InsurancePlan', 'insurance_name', insurance_name))

        return plan  