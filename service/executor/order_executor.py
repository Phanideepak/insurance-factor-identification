

from api.dto.dto import CreateOrderRequest, OrderPaymentRequest
from sqlalchemy.orm import Session

from service.services.order_service import OrderService
from service.utils.validation_utils import ValidationUtils


class OrderExecutor:
    def place_order(request : CreateOrderRequest, agent_email, db : Session):
        ValidationUtils.isZero(request.customer_id, 'customer_id')
        ValidationUtils.isZero(request.insurance_detail_id, 'insurance_detail_id')
        ValidationUtils.isEmpty(request.premium_type, 'premium_type')
        ValidationUtils.isEmpty(agent_email, 'agent_email')

        return OrderService.place_order(request, agent_email, db)
    
    def proceed_to_payment(request : OrderPaymentRequest, customer_email, db : Session):
        ValidationUtils.isZero(request.order_id, 'order_id')
        ValidationUtils.isZero(request.amount_paid, 'amount_paid')
        ValidationUtils.isEmpty(customer_email, 'customer_email')

        return OrderService.proceed_to_payment(request, customer_email, db)
    
    def get_by_id(order_id, db : Session):
        ValidationUtils.isZero(order_id, 'id')

        return OrderService.get_by_id(order_id, db)
    
    def approve_order(order_id, agent_email, db : Session):
        ValidationUtils.isZero(order_id, 'id')
        ValidationUtils.isEmpty(agent_email, 'agent_email')

        return OrderService.approve_order(order_id, agent_email, db)