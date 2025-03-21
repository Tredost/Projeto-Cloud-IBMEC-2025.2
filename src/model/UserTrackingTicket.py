from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserTrackingTicker(Base):
    __tablename__ = 'user_tracking_ticker'

    id: int
    symbol: str

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String)
