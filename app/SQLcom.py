from sqlalchemy import create_engine, Column, String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker
from models import Admin, Customer

# Настройки подключения к базе данных PostgreSQL
host = "192.168.30.92"
database = "TTKTarif"
user = "postgres"
password = "mypassword"
port = "5435"

# Создание строки подключения к базе данных
engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}",
                       client_encoding="utf-8",
                       connect_args={"options": "-c search_path=public"})



# Создание сессии для взаимодействия с базой данных
Session = sessionmaker(bind=engine)

# Функция для получения сессии
def get_session():
    return Session()










# Функция для получения фамилии человека из таблицы admins по логину
def get_fio_from_admins(login):
    try:
        session = get_session()
        admin = session.query(Admin).filter(Admin.login == login).first()
        if admin:
            return admin.fio.split()[0]  # возвращаем только фамилию
        else:
            return None
    except SQLAlchemyError as error:
        print("Error executing SQL query:", error)
        return None

# Функция для получения фамилии человека из таблицы customers по номеру num
def get_fio_from_customers(num):
    try:
        session = get_session()
        customer = session.query(Customer).filter(Customer.num_dog == num).first()
        if customer:
            return customer.fio.split()[0]
        else:
            return None
    except SQLAlchemyError as error:
        print("Error executing SQL query:", error)
        return None

# Пример использования функций
admin_login = "admin1"
admin_surname = get_fio_from_admins(admin_login)
if admin_surname:
    print(f"Фамилия администратора с логином {admin_login}: {admin_surname}")
else:
    print(f"Администратор с логином {admin_login} не найден.")

customer_num = "516123456"
customer_surname = get_fio_from_customers(customer_num)
if customer_surname:
    print(f"Фамилия клиента с номером {customer_num}: {customer_surname}")
else:
    print(f"Клиент с номером {customer_num} не найден.")




# создаем функцию для добавления записи в таблицу
def add_tg_id(num_dog, telegram_id):
    try:
        # создаем сессию
        Session = sessionmaker(bind=engine)
        session = Session()

        # ищем запись в базе по num_dog
        customer = session.query(Customer).filter(Customer.num_dog == num_dog).first()

        if customer:
            # если запись найдена, обновляем telegram_id
            customer.telegram_id = telegram_id
        else:
            # если запись не найдена, создаем новую запись
            customer = Customer(telegram_id=telegram_id, num_dog=num_dog)
            session.add(customer)

        # коммитим изменения
        session.commit()

        # возвращаем id добавленной записи
        return customer.id

    except SQLAlchemyError as e:
        # откатываем изменения при ошибке
        session.rollback()
        print(f"Ошибка: {e}")
        return None

    finally:
        # закрываем сессию
        session.close()


 # def get_profile(num):
 #    try:
 #        session = get_session()
 #        customer = session.query(Customer).filter(Customer.num_dog == num).first()
 #        if customer:
 #            return f"ФИО"
 #        else:
 #            return None
 #    except SQLAlchemyError as error:
 #            print("Error executing SQL query:", error)
 #            return None