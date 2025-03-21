from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from models import UserConfiguration  # Supondo que você tenha suas classes de modelo definidas em um arquivo chamado 'models.py'

# Criação do motor de banco de dados
engine = create_engine('sqlite:///database.db')  # Você pode usar outro banco de dados aqui, conforme necessário

# Criar a fábrica de sessões
Session = sessionmaker(bind=engine)

class UserConfigurationRepository:
    def __init__(self):
        self.session = Session()

    def save(self, configuration: UserConfiguration):
        self.session.add(configuration)
        self.session.commit()

    def find_by_id(self, id: int):
        return self.session.query(UserConfiguration).filter(UserConfiguration.id == id).first()

    def find_all(self):
        return self.session.query(UserConfiguration).all()

    def delete(self, configuration: UserConfiguration):
        self.session.delete(configuration)
        self.session.commit()

    def close(self):
        self.session.close()

# Exemplo de como utilizar
repository = UserConfigurationRepository()

# Criando uma nova configuração
new_config = UserConfiguration(loss_percent=10.0, profit_percent=5.0, quantity_per_order=100.0)
repository.save(new_config)

# Buscando uma configuração por id
config = repository.find_by_id(1)
print(config)
