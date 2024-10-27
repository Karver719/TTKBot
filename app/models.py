from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

# Создание базового класса для моделей
Base = declarative_base()

# Модель таблицы admins
class Admin(Base):
    __tablename__ = "admins"
    login = Column(String, primary_key=True)
    fio = Column(String)

# Модель таблицы num_dog
class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    num_dog = Column(Text)  # Соответствует TEXT в PostgreSQL
    fio = Column(Text, nullable=False)  # Соответствует TEXT NOT NULL
    telephone = Column(String(20))  # Соответствует VARCHAR(20)
    mail = Column(String(100))  # Соответствует VARCHAR(100)
    telegram_id = Column(Text)  # Соответствует TEXT

    def __init__(self, num_dog, fio, telephone=None, mail=None, telegram_id=None):
        self.num_dog = num_dog
        self.fio = fio
        self.telephone = telephone
        self.mail = mail
        self.telegram_id = telegram_id

Base = declarative_base()

