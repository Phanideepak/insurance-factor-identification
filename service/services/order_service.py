from api.dto.dto import CreateOrderRequest, OrderPaymentRequest
from sqlalchemy.orm import Session

from api.exception.errors import StateMachineException, ValidationException
from repository.insurance.service.agent_repo_service import AgentRepoService
from repository.insurance.service.customer_repo_service import CustomerRepoService
from repository.insurance.service.insurance_plan_repo_service import InsurancePlanRepoService
from repository.insurance.service.life_insurance_detail_repo_service import LifeInsuranceDetailRepoService
from repository.insurance.service.order_repo_service import OrderRepoService
from repository.insurance.service.task_repo_service import TaskRepoService
from repository.insurance.service.user_repo_service import UserRepoService
from service.mapper.mapper import Mapper, ResponseMapper
from service.utils.response_util import ResponseUtils

class OrderService:
    def place_order(request : CreateOrderRequest, agent_email, db : Session):
        user = UserRepoService.validate_and_get_by_email(agent_email, db)
        agent = AgentRepoService.validate_and_get_by_email(agent_email, db)
        customer = CustomerRepoService.validate_and_get_by_id(request.customer_id, db)
        insurance_detail = LifeInsuranceDetailRepoService.validate_and_get_by_id(request.insurance_detail_id, db)
        insurance = InsurancePlanRepoService.validate_and_get_by_id(insurance_detail.insurance_id, db)

        amount_to_pay = insurance_detail.basic_sum_assured / insurance_detail.duration
  
        if request.premium_type == 'QUARTERLY':
           amount_to_pay = 3 * amount_to_pay 
        
        if request.premium_type == 'HALF_YEARLY':
            amount_to_pay = 6 * amount_to_pay
        
        if request.premium_type == 'ANNUAL':
            amount_to_pay = 12 * amount_to_pay

        order_persisted = OrderRepoService.insert(Mapper.toOrder(customer, insurance, insurance_detail, 'UNDER_REVIEW', user, amount_to_pay, request.premium_type), db)

        return ResponseUtils.wrap(ResponseMapper.toOrderDto(order_persisted, agent, insurance, insurance_detail, request.premium_type, amount_to_pay, customer, user))
    
    def get_by_id(order_id, db):
        order = OrderRepoService.validate_and_get_by_id(order_id, db)
        created_by = UserRepoService.validate_and_get_by_id(order.created_by, db)
        agent = AgentRepoService.validate_and_get_by_email(created_by.email, db)
        insurance = InsurancePlanRepoService.validate_and_get_by_id(order.insurance_id, db)
        insurance_detail = LifeInsuranceDetailRepoService.validate_and_get_by_id(order.sub_insurance_id, db)
        customer = CustomerRepoService.validate_and_get_by_id(order.customer_id, db)
        approved_by = UserRepoService.fetch_by_id(order.approved_by, db)

        return ResponseUtils.wrap(ResponseMapper.toOrderDto(order, agent, insurance, insurance_detail, order.premium_type, order.amount_to_pay, customer, created_by, approved_by))
    
    def approve_order(order_id, admin_email, db : Session):
        order = OrderRepoService.validate_and_get_by_id(order_id, db)

        if order.order_status.name != 'UNDER_REVIEW':
            raise StateMachineException('Order State Machine Broken: Order Should be `UNDER_REVIEW`')

        admin_user = UserRepoService.validate_and_get_by_email(admin_email, db)
        order.approved_by = admin_user.id
        order.order_status = 'PENDING'

        OrderRepoService.update(order, db)

        created_by = UserRepoService.validate_and_get_by_id(order.created_by, db)
        agent = AgentRepoService.validate_and_get_by_email(created_by.email, db)
        insurance = InsurancePlanRepoService.validate_and_get_by_id(order.insurance_id, db)
        insurance_detail = LifeInsuranceDetailRepoService.validate_and_get_by_id(order.sub_insurance_id, db)
        customer = CustomerRepoService.validate_and_get_by_id(order.customer_id, db)
        approved_by = admin_user
        

        return ResponseUtils.wrap(ResponseMapper.toOrderDto(order, agent, insurance, insurance_detail, order.premium_type, order.amount_to_pay, customer, created_by, approved_by))

    def proceed_to_payment(request : OrderPaymentRequest, customer_email, db : Session):
            order = OrderRepoService.validate_and_get_by_id(request.order_id, db)

            if order.order_status.name not in ['PENDING', 'PAYMENT_FAILED']:
               raise StateMachineException('Order State Machine Broken: Order Should be `PENDING`') 
            
            if request.amount_paid < order.amount_to_pay:
                raise ValidationException('Insufficient Funds')
            
            refund_amount = request.amount_paid - order.amount_to_pay

            if refund_amount:
                print('refund amount: ',refund_amount)
            
            order.amount_paid = order.amount_to_pay
            order.payment_status = 'PAID'
            order.order_status = 'CONFIRMED'

            OrderRepoService.update(order, db)

            TaskRepoService.insert(Mapper.toTask(order, 'INFORCE'),db)

            created_by = UserRepoService.validate_and_get_by_id(order.created_by, db)
            agent = AgentRepoService.validate_and_get_by_email(created_by.email, db)
            insurance = InsurancePlanRepoService.validate_and_get_by_id(order.insurance_id, db)
            insurance_detail = LifeInsuranceDetailRepoService.validate_and_get_by_id(order.sub_insurance_id, db)
            customer = CustomerRepoService.validate_and_get_by_id(order.customer_id, db)
            approved_by = UserRepoService.fetch_by_id(order.approved_by, db) 

            return ResponseUtils.wrap(ResponseMapper.toOrderDto(order, agent, insurance, insurance_detail, order.premium_type, order.amount_to_pay, customer, created_by, approved_by))