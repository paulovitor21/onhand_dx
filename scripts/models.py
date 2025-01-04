from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DOUBLE_PRECISION, String, Date

Base = declarative_base()

class OnhandRecord(Base):
    
    __tablename__= 'table_onhand'

    
    id = Column(Integer, primary_key=True, index=True)
    file_date = Column(name="file_date", type_=Date)
    org = Column(name='org', type_=String)
    item = Column(name='item', type_=String)
    uit = Column(name='uit', type_=String)
    desc = Column(name='desc', type_=String)
    subinv = Column(name='subinv', type_=String)
    locator = Column(name='locator', type_=String)
    onhand_qty = Column(name='onhand_qty', type_=DOUBLE_PRECISION)
    planner = Column(name='planner', type_=String)
    purchaser = Column(name='purchaser', type_=String)
    hash_id = Column(String, unique=True)