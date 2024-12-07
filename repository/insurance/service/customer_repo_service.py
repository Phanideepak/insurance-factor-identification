from sqlalchemy.orm import Session

from api.exception.errors import DataNotFoundException
from repository.insurance.model.insurance import Customer
from service.utils.message_utils import MessageUtils


class CustomerRepoService:
    
    def insert(customer, db : Session):
        db.add(customer)
        db.commit()
    
    def update(customer, db : Session):
        db.query(Customer).filter(Customer.id == customer.id).update({Customer.firstname : customer.firstname, Customer.lastname : customer.lastname, Customer.healthy : customer.healthy, Customer.life_style: customer.life_style, Customer.occupation : customer.occupation, Customer.occupation_type : customer.occupation_type, Customer.city : customer.city, Customer.pincode : customer.pincode, Customer.lat : customer.lat, Customer.lng : customer.lng, Customer.first_line : customer.first_line, Customer.last_line : customer.last_line, Customer.land_mark : customer.land_mark, Customer.email : customer.email, Customer.phone  : customer.phone})
        db.commit()
    
    def fetch_by_id(id, db : Session):
        return db.query(Customer).filter(Customer.id == id).first()
    
    def fetch_all(db : Session):
        return db.query(Customer).filter(Customer.is_deleted == False).all()

    @classmethod
    def validate_and_get_by_id(cls, id, db : Session):
        customer = cls.fetch_by_id(id, db)
        if customer is None:
            raise DataNotFoundException(MessageUtils.entity_not_found('Customer', 'id', id))

        return customer


    @classmethod
    def validate_and_get_all(cls, db : Session):
        customers = cls.fetch_all(db)
        if not customers:
            raise DataNotFoundException(MessageUtils.entities_not_found('Customers'))

        return customers


    def delete_by_id(id, db : Session):
        db.query(Customer).filter(Customer.id == id).update({Customer.is_deleted : True})
        db.commit()