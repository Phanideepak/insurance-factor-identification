from sqlalchemy.orm import Session

from api.exception.errors import DataNotFoundException
from repository.insurance.model.insurance import Order
from service.utils.message_utils import MessageUtils


class OrderRepoService:
    
    def insert(order, db : Session):
        db.add(order)
        db.commit()
        return order
    
    def update(order, db : Session):
        db.query(Order).filter(Order.id == order.id).update({Order.customer_id : order.customer_id, Order.insurance_id : order.insurance_id, Order.sub_insurance_id : order.sub_insurance_id, Order.amount_to_pay : order.amount_to_pay, Order.amount_paid : order.amount_paid, Order.order_status : order.order_status, Order.payment_status : order.payment_status, Order.created_by : order.created_by, Order.approved_by : order.approved_by})
        db.commit()
    
    def fetch_by_id(id, db : Session):
        return db.query(Order).filter(Order.id == id).first()
    
    def fetch_all(db : Session):
        return db.query(Order).all()

    @classmethod
    def validate_and_get_by_id(cls, id, db : Session):
        order = cls.fetch_by_id(id, db)
        if order is None:
            raise DataNotFoundException(MessageUtils.entity_not_found('Order', 'id', id))

        return order


    @classmethod
    def validate_and_get_all(cls, db : Session):
        orders = cls.fetch_all(db)
        if not orders:
            raise DataNotFoundException(MessageUtils.entities_not_found('Orders'))

        return orders


    def delete_by_id(id, db : Session):
        db.query(Order).filter(Order.id == id).delete()
        db.commit()