from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from dataclasses import dataclass

Base = declarative_base()

@dataclass
class User(Base):
    __tablename__ = 'user'

    id: int
    login: str
    password: str
    binance_api_key: str
    binance_secret_key: str
    saldo_inicio: float
    configurations: list
    tracking_tickers: list

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String)
    password = Column(String)
    binance_api_key = Column(String)
    binance_secret_key = Column(String)
    saldo_inicio = Column(Float)

    # Relacionamentos OneToMany
    configurations = relationship("UserConfiguration", back_populates="user")
    tracking_tickers = relationship("UserTrackingTicker", back_populates="user")

# Definindo a classe de UserConfiguration como exemplo
class UserConfiguration(Base):
    __tablename__ = 'user_configuration'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="configurations")

# Definindo a classe de UserTrackingTicker como exemplo
class UserTrackingTicker(Base):
    __tablename__ = 'user_tracking_ticker'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="tracking_tickers")
