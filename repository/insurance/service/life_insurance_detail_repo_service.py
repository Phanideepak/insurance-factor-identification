from api.exception.errors import DataNotFoundException
from repository.insurance.model.insurance import LifeInsuranceDetail
from service.utils.message_utils import MessageUtils
from sqlalchemy.orm import Session

class LifeInsuranceDetailRepoService:

    def add(detail, db : Session):
        db.add(detail)
        db.commit()
    
    def update(detail : LifeInsuranceDetail, db : Session):
        db.query(LifeInsuranceDetail).filter(LifeInsuranceDetail.id == detail.id, LifeInsuranceDetail.plan_code == detail.plan_code).update({LifeInsuranceDetail.insurance_id : detail.insurance_id, LifeInsuranceDetail.basic_sum_assured : detail.basic_sum_assured, LifeInsuranceDetail.duration : detail.duration, LifeInsuranceDetail.interest : detail.interest, LifeInsuranceDetail.interest_type : detail.interest_type })
        db.commit()
    
    def delete_by_insurance_id(insurance_id, db : Session):
        db.query(LifeInsuranceDetail).filter(LifeInsuranceDetail.insurance_id == insurance_id).delete()
        db.commit()
    
    def fetch_by_id(id, db : Session):
        return db.query(LifeInsuranceDetail).filter(LifeInsuranceDetail.id == id).first()
    
    def validate_and_get_by_id(id, db : Session):
        detail = db.query(LifeInsuranceDetail).filter(LifeInsuranceDetail.id == id).first()
        if detail is None:
           raise DataNotFoundException(MessageUtils.entity_not_found('LifeInsuranceDetail', 'id', id))

        return detail

    def fetch_by_insurance_id(insurance_id, db : Session):
        return db.query(LifeInsuranceDetail).filter(LifeInsuranceDetail.insurance_id == insurance_id).all() 
    
    def validate_and_get_by_insurance_id(insurance_id, db : Session):
        details = db.query(LifeInsuranceDetail).filter(LifeInsuranceDetail.insurance_id == insurance_id).all() 

        if not details:
            raise DataNotFoundException(MessageUtils.entity_not_found('LifeInsuranceDetails', 'insurance_id', insurance_id))
        
        return details

