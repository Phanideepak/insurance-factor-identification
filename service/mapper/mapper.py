from typing import List
from repository.ems.model.ems import User, Department, Address, Employee
from api.dto.dto import UserDto, DepartmentDto, AddressDto, EmployeeDto


def employeeModelToEmployeeDto(emp : Employee, dept : Department, created_user : User, deleted_user : User, approved_user: User):
    empDto =  EmployeeDto(id = emp.id, eid = emp.eid, firstname = emp.firstname, 
                       lastname = emp.lastname, contact = emp.contact,
                       approval_status = ('Not Approved','Approved') [emp.is_approved], 
                       approved_by = userModelToUserDto(approved_user),
                       designation = emp.designation,
                       office_mail = emp.office_mail,
                       is_deleted = emp.is_deleted,
                       deleted_by = userModelToUserDto(deleted_user), 
                       created_by = userModelToUserDto(created_user), 
                       dept = departmentModelToDepartmentDto(dept)
                       )
    
    if emp.approved_at is not None:
        empDto.approved_at = emp.approved_at.strftime("%m/%d/%Y, %H:%M:%S")

    if emp.deleted_at is not None:
        empDto.deleted_at = emp.deleted_at.strftime("%m/%d/%Y, %H:%M:%S")
    
    return empDto


def departmentModelToDepartmentDto(dept : Department):
    return DepartmentDto(id = dept.id, name = dept.name, description=dept.description,
                          approval_status = ('Not Approved','Approved') [dept.is_approved] 
                          ,is_deleted = dept.is_deleted )

def departmentCacheToDepartmentDto(dept : dict):
    return DepartmentDto(id = dept['id'], name = dept['name'], description=dept['description'],
                          approval_status = ('Not Approved','Approved') [dept['is_approved']] 
                          ,is_deleted = dept['is_deleted'])

def departmentModelToDepartmentDtoList(depts : List):
    deptDtos = []

    for dept in depts:
        deptDtos.append(departmentModelToDepartmentDto(dept))

    return deptDtos

def departmentCacheToDepartmentDtoList(depts : List[dict]):
    deptDtos = []

    for dept in depts:
        deptDtos.append(departmentCacheToDepartmentDto(dept))

    return deptDtos

def userModelToUserDto(user : User):
    if user is None:
        return None
    return UserDto(id = user.id, firstname = user.firstname, lastname = user.lastname, email = user.email, role = user.role.name)

def userModelToUserDtoList(users : List):
    userDtos = []

    for user in users:
        userDtos.append(userModelToUserDto(user))

    return userDtos

def addressModelToAddressDto(address : Address):
    return AddressDto(id = address.id, eid = address.eid, first_line = address.first_line, second_line = address.second_line, land_mark = address.land_mark, phone = address.phone, city = address.city, pincode = address.pincode, state = address.state, is_primary = address.is_primary)

def addressModelToAddressDtoList(addresses : List):
    addressDtos = []

    for address in addresses:
        addressDtos.append(addressModelToAddressDto(address))

    return addressDtos