from typing import List
from datetime import datetime
from api.dto.dto import AddCustomerRequest, AddInsuranceRequest, AgentDto, CustomerDto, InsuranceDto, LifeInsuranceDto, LifeInsuranceInput, InsurancePremiumDetailDto, OrderDto, UserDto
from repository.insurance.model.insurance import Customer, InsurancePlan, LifeInsuranceDetail, Agent, Order, Task, User


class Mapper:
    def toInsurancePlan(request : AddInsuranceRequest):
        return InsurancePlan(insurance_name= request.insurance_name, insurance_type = request.insurance_type, description = request.description)

    def toLifeInsuranceDetail(insurance : InsurancePlan, detail : LifeInsuranceInput):
        return LifeInsuranceDetail(insurance_id = insurance.id, basic_sum_assured = detail.basic_sum_assured, interest = detail.interest, interest_type = detail.interest_type, duration=detail.duration, plan_code = f'{insurance.insurance_name}-{detail.duration}'.replace(' ', '_').upper())

    def toCustomer(request : AddCustomerRequest):
        return Customer(firstname=request.firstname, lastname= request.lastname, healthy=request.healthy, life_style=request.life_style, occupation=request.occupation, occupation_type=request.occupation_type, city=request.city, pincode=request.pincode, lat = request.lat, lng = request.lng, first_line=request.first_line, last_line=request.last_line, land_mark=request.land_mark, email = request.email, phone = request.phone)
    
    def toAgent(request : AddCustomerRequest):
        return Agent(firstname=request.firstname, lastname= request.lastname, email = request.email, phone = request.phone)
    
    def toTask(order : Order, task_status):
        return Task(order_id = order.id, premium_amount_to_pay = order.amount_to_pay, premium_type= order.premium_type.name, task_status = task_status, premium_amount_paid = order.amount_paid, payment_status = order.payment_status, paid_at = datetime.now())

    def toOrder(customer ,insurance, insurance_detail, status, agent_user, amount_to_pay, premium_type):
        return Order(customer_id = customer.id, insurance_id = insurance.id, sub_insurance_id= insurance_detail.id, amount_to_pay = amount_to_pay, order_status = status, created_by=agent_user.id, premium_type = premium_type)
class ResponseMapper:

    def toUserDto(user : User):
        if not user:
            return None 
        return UserDto(id = user.id, firstname = user.firstname, lastname = user.lastname, email = user.email, role = user.role.name)

    @classmethod
    def toOrderDto(cls, order : Order, agent : Agent, insurance : InsurancePlan, insurance_detail : LifeInsuranceDetail, premium_type, premium_amount, customer, created_by, approved_by = None):
        return OrderDto(order_id = order.id, status = order.order_status.name, payment_status = order.payment_status.name, premium_type = premium_type, agent = cls.toAgentDto(agent), insurance = cls.toInsurancePremiumDetailDto(insurance, insurance_detail, premium_type, premium_amount), customer = cls.toCustomerDto(customer), created_by = cls.toUserDto(created_by), approved_by = cls.toUserDto(approved_by))

    def toInsurancePremiumDetailDto(insurance : InsurancePlan, insurance_detail : LifeInsuranceDetail, premium_type, premium_amount):
        return InsurancePremiumDetailDto(insurance_id = insurance.id, insurance_name = insurance.insurance_name, insurance_type= insurance.insurance_type, description = insurance.description, basic_sum_assured= insurance_detail.basic_sum_assured, duration = insurance_detail.duration, interest= insurance_detail.interest, interest_type= insurance_detail.interest_type, plan_code= insurance_detail.plan_code, premium_amount= premium_amount, premium_type= premium_type)

    def toAgentDto(agent : Agent):
        return AgentDto(id = agent.id, firstname=agent.firstname, lastname=agent.lastname, email=agent.email, phone = agent.phone) 
    
    @classmethod
    def toAgentDtos(cls, agents : List[Agent]):
        return [cls.toAgentDto(agent) for agent in agents]   
    
    def toCustomerDto(customer : Customer):
        return CustomerDto(id = customer.id, firstname=customer.firstname, lastname=customer.lastname, healthy=customer.healthy.name, life_style=customer.life_style.name, occupation=customer.occupation, occupation_type=customer.occupation_type.name, city = customer.city, pincode = customer.pincode, lat = customer.lat, lng = customer.lng, first_line=customer.first_line, last_line=customer.last_line, land_mark=customer.land_mark, email=customer.email, phone = customer.email) 
    
    @classmethod
    def toCustomerDtos(cls, customers : List[Customer]):
        return [cls.toCustomerDto(customer) for customer in customers]
    
    def toLifeInsuranceDto(detail : LifeInsuranceDetail):
        return LifeInsuranceDto(id = detail.id, basic_sum_assured = detail.basic_sum_assured, duration = detail.duration, interest = detail.interest, interest_type = detail.interest_type, plan_code = detail.plan_code)

    @classmethod
    def toLifeInsuranceDtos(cls, details : List[LifeInsuranceDetail]):
        return [cls.toLifeInsuranceDto(detail) for detail in details]

    @classmethod
    def toInsuranceDto(cls, insurance : InsurancePlan, detail_list : List[LifeInsuranceDetail]):
        return InsuranceDto(insurance_id = insurance.id, insurance_name = insurance.insurance_name, insurance_type = insurance.insurance_type, description = insurance.description, life_insurance_details = cls.toLifeInsuranceDtos(detail_list))