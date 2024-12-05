from repository.ems.service.address_repo_service import AddressRepoService
from repository.ems.service.employment_repo_service import EmployeeRepoService
from repository.ems.model.ems import Address
from api.dto.dto import AddAddressRequest, UpdateAddressRequest
from api.exception.errors import NotModifiedException, ServiceException
from sqlalchemy.orm import Session
from service.utils.response_util import ResponseUtils
from service.mapper.mapper import addressModelToAddressDto, addressModelToAddressDtoList

from service.utils.validation_utils import ValidationUtils




class AddressService:
    def add(request : AddAddressRequest, logged_user : str, db : Session):
        emp = EmployeeRepoService.validateAndGetByOfficeMail(logged_user, db)
        try:
            AddressRepoService.save(Address(eid = emp.id, first_line = request.first_line, second_line = request.second_line, phone = request.phone, land_mark = request.land_mark, city = request.city, state = request.state, pincode = request.pincode), db)
        except Exception as e:
            raise ServiceException(str(e))
        
        return ResponseUtils.wrap('added successfully')
    

    def update(request : UpdateAddressRequest, logged_user : str,  db : Session):
        emp = EmployeeRepoService.validateAndGetByOfficeMail(logged_user, db)
        address = AddressRepoService.validateAndGetByIdAndEid(request.id, emp.id, db)
        
        is_updated = False

        if request.first_line != address.first_line:
            address.first_line = request.first_line
            is_updated = True
        
        if request.second_line != address.second_line:
            address.second_line = request.second_line
            is_updated = True
        
        if request.land_mark != address.land_mark:
            address.land_mark = request.land_mark
            is_updated = True

        if  request.phone != address.phone:
            address.phone = request.phone
            is_updated = True
        
        if request.city != address.city:
            address.city = request.city
            is_updated = True
        
        if request.pincode != address.pincode:
            address.pincode = request.pincode
            is_updated = True
        
        if request.state != address.state:
            address.state = request.state

        
        if not is_updated:
           raise NotModifiedException()

        try:
            AddressRepoService.update(address,db)
        except Exception as e:
            raise ServiceException(str(e))
        
        return ResponseUtils.wrap('updated successfully')


    def getById(id : int, logged_user : str, db : Session):
        emp = EmployeeRepoService.validateAndGetByOfficeMail(logged_user, db)
        address = AddressRepoService.validateAndGetByIdAndEid(id, emp.id, db)

        return ResponseUtils.wrap(addressModelToAddressDto(address))
    
    def fetchById(id : int, logged_user : str, db : Session):
        emp = EmployeeRepoService.validateAndGetByOfficeMail(logged_user, db)
        address = AddressRepoService.fetchByIdAndEid(id, emp.id, db)

        return addressModelToAddressDto(address)
    
    
    def getAll(logged_user : str, db : Session):
        emp = EmployeeRepoService.validateAndGetByOfficeMail(logged_user, db)
        addresses = AddressRepoService.fetchByEid(emp.id, db)
        return ResponseUtils.wrap(addressModelToAddressDtoList(addresses))
    
    def fetchAll(logged_user : str, db : Session):
        emp = EmployeeRepoService.validateAndGetByOfficeMail(logged_user, db)
        addresses = AddressRepoService.fetchByEid(emp.id, db)

        return addressModelToAddressDtoList(addresses)
    

    def deleteById(id : int, logged_user : str, db : Session):
        emp = EmployeeRepoService.validateAndGetByOfficeMail(logged_user, db)
        address = AddressRepoService.validateAndGetByIdAndEid(id, emp.id, db)

        try:
            AddressRepoService.deleteByIdAndEid(id, emp.id, db)
        except Exception as e:
            raise ServiceException(str(e))

        return ResponseUtils.wrap('Deleted successfully')
    
    def make_primary(id : int, logged_user : str, db : Session):
        emp = EmployeeRepoService.validateAndGetByOfficeMail(logged_user, db)
        address = AddressRepoService.validateAndGetByIdAndEid(id, emp.id, db)
        
        if address.is_primary:
            ValidationUtils.isTrue(not address.is_primary, 'Already Primary')

        try:
            AddressRepoService.makePrimary(id, emp.id, db)
        except Exception as e:
            raise ServiceException(str(e))

        return ResponseUtils.wrap('Address made primary successfully')