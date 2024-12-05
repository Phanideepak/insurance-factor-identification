from sqlalchemy.orm import Session
from api.exception.errors import DataNotFoundException
from repository.ems.model.ems import Address
from service.utils.message_utils import MessageUtils


class AddressRepoService:
    def save(address : Address, db : Session):
        db.query(Address).filter(Address.eid == address.eid).update({Address.is_primary : False})
        db.add(address)
        db.commit()
    
    def update(address : Address, db : Session):
        db.query(Address).filter(Address.id == address.id, Address.eid == address.eid).update({
                                      Address.first_line : address.first_line,
                                      Address.second_line : address.second_line,
                                      Address.land_mark : address.land_mark,
                                      Address.phone : address.phone,
                                      Address.pincode : address.pincode,
                                      Address.city : address.city,
                                      Address.state : address.state
                                      })
        db.commit()

    def fetchByIdAndEid(id : int, eid : int,  db : Session):
        return db.query(Address).filter(Address.id == id, Address.eid == eid).first()
    
    def fetchByEid(eid : int,  db : Session):
        return db.query(Address).filter(Address.eid == eid).all()

    def validateAndGetByIdAndEid(id : int, eid : int,  db : Session):
        emp = db.query(Address).filter(Address.id == id, Address.eid == eid).first()
        if emp is None:
            raise DataNotFoundException(MessageUtils.entity_not_found_two('Address','id',id, 'eid', eid))
        return emp
    
    def validateAndGetByEid(eid : int,  db : Session):
        emps = db.query(Address).filter(Address.eid == eid).all()
        if len(emps) == 0:
            raise DataNotFoundException(MessageUtils.entity_not_found_one('Addresses','eid',eid))
        return emps
    
    
    def makePrimary(id : int, eid : int, db : Session):
        db.query(Address).filter(Address.eid == eid).update({Address.is_primary : False})
        db.commit()
        db.query(Address).filter(Address.id == id, Address.eid == eid).update({Address.is_primary : True})
        db.commit()
    
    def deleteByIdAndEid(id: int, eid, db : Session):
        db.query(Address).filter(Address.id == id, Address.eid == eid).delete()
        db.commit()