from sqlalchemy import Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserConfiguration(Base):
    __tablename__ = 'user_configuration'

    id: int
    loss_percent: float
    profit_percent: float
    quantity_per_order: float

    id = Column(Integer, primary_key=True, autoincrement=True)
    loss_percent = Column(Float)
    profit_percent = Column(Float)
    quantity_per_order = Column(Float)
