from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import User  # Supondo que você tenha suas classes de modelo definidas em um arquivo chamado 'models.py'

# Criação do motor de banco de dados
engine = create_engine('sqlite:///database.db')  # Você pode usar outro banco de dados aqui, conforme necessário

# Criar a fábrica de sessões
Session = sessionmaker(bind=engine)

class UserRepository:
    def __init__(self):
        self.session = Session()

    def save(self, user: User):
        self.session.add(user)
        self.session.commit()

    def find_by_id(self, id: int):
        return self.session.query(User).filter(User.id == id).first()

    def find_all(self):
        return self.session.query(User).all()

    def delete(self, user: User):
        self.session.delete(user)
        self.session.commit()

    def close(self):
        self.session.close()

# Exemplo de como utilizar
repository = UserRepository()

# Criando um novo usuário
new_user = User(login="user1", password="password", binance_api_key="api_key", binance_secret_key="secret_key", saldo_inicio=1000.0)
repository.save(new_user)

# Buscando um usuário por id
user = repository.find_by_id(1)
print(user)
