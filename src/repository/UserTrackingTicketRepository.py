from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model import UserTrackingTicker  

# Criação do motor de banco de dados
engine = create_engine('sqlite:///database.db')  # Você pode usar outro banco de dados aqui, conforme necessário

# Criar a fábrica de sessões
Session = sessionmaker(bind=engine)

class UserTrackingTickerRepository:
    def __init__(self):
        self.session = Session()

    def save(self, ticker: UserTrackingTicker):
        self.session.add(ticker)
        self.session.commit()

    def find_by_id(self, id: int):
        return self.session.query(UserTrackingTicker).filter(UserTrackingTicker.id == id).first()

    def find_all(self):
        return self.session.query(UserTrackingTicker).all()

    def delete(self, ticker: UserTrackingTicker):
        self.session.delete(ticker)
        self.session.commit()

    def close(self):
        self.session.close()

# Exemplo de como utilizar
repository = UserTrackingTickerRepository()

# Criando um novo ticker de rastreamento
new_ticker = UserTrackingTicker(symbol="BTCUSDT")  # Supondo que o campo 'symbol' seja uma string
repository.save(new_ticker)

# Buscando um ticker de rastreamento por id
ticker = repository.find_by_id(1)
print(ticker)
