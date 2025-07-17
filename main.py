import os
# from dotenv import load_dotenv

# Загружаем переменные из .env файла
# load_dotenv()
# 
# POOL = pooling.MySQLConnectionPool(
#     host=os.environ.get('DB_HOST'),
#     port=os.environ.get('DB_PORT'),
#     user=os.environ.get('DB_USER'),
#     password=os.environ.get('DB_PASSWORD'),
#     pool_name='pool1',
#     pool_size=5)


from config import engine, get_session
from models import Base, Product, Manager, Buyer, Email, Order
import fakerdata as fake
from order_service import create_order, display_all_orders, display_orders_id

if __name__ == '__main__':
    Base.metadata.create_all(engine)

session = get_session()

''' Функції роботи з даними (додавання, видалення, оновлення)'''


def add_products():
    try:
        for _ in range(12):
            product = Product(name=fake.get_product())
            session.add(product)
            session.commit()
            session.refresh(product)
            print(f'{product.id} - {product.name} додано.')
    finally:
        session.close()


def add_manager():
    try:
        manager = Manager(name=fake.get_person_name())
        session.add(manager)
        session.commit()
        session.refresh(manager)
        print(f'Manager added: - {manager.id} - {manager.name}.')
    finally:
        session.close()


def add_buyer():
    try:
        buyer = Buyer(name=fake.get_person_name())
        buyer.email = Email(email=fake.get_email())
        session.add(buyer)
        session.commit()
        session.refresh(buyer)
        print(f'Buyer added: {buyer.id} - {buyer.name} - {buyer.email.email}.')
    finally:
        session.close()


def add_quantity_product():
    print('Функція видалення...')


def change_product(product_id, name):
    """Змінити назву товару"""
    try:
        product = session.query(Product).filter_by(id=product_id).first()
        product.name = name
        session.commit()
        session.refresh(product)
        print(f'{product.id} - {product.name} оновлено.')
    finally:
        session.close()


def change_manager(manager_id, name):
    """Змінити назву товару"""
    try:
        manager = session.query(Manager).filter_by(id=manager_id).first()
        manager.name = name
        session.commit()
        session.refresh(manager)
        print(f'Дані продавця {manager.id} - {manager.name} оновлено.')
    finally:
        session.close()


def change_buyer(buyer_id, name):
    """Змінити назву товару"""
    try:
        buyer = session.query(Buyer).filter_by(id=buyer_id).first()
        buyer.name = name
        session.commit()
        session.refresh(buyer)
        print(f'Дані покупця {buyer.id} - {buyer.name} оновлено.')
    finally:
        session.close()


# Фукнкцію виводу даних

def display_all_products():
    """Вивести список всіх товарів"""
    try:
        products = session.query(Product.id, Product.name)
        for product_id, product_name in products:
            print(product_id, product_name)
    finally:
        session.close()


def display_all_managers():
    """Вивести список всіх товарів"""
    try:
        managers = session.query(Manager.id, Manager.name)
        for manager_id, manager_name in managers:
            print(manager_id, manager_name)
    finally:
        session.close()


def display_all_buyers():
    """Вивести список всіх покупців"""
    try:
        buyers = (
            session.query(Buyer.id, Buyer.name, Email.email)
            # .join(Email, Buyer.email)
            .join(Email, Buyer.email_id == Email.id)
            .all()
        )
        for buyer_id, buyer_name, buyer_email in buyers:
            print(buyer_id, buyer_name, buyer_email)

    finally:
        session.close()


# функії роботи з меню

def menu_editing_data():  # dictionaries():
    '''Меню відбору даних для редагування'''
    while True:
        choice = int(input("""
                    1. Товари
                    2. Менеджери
                    3. Покупці
                    4. Back
                    """))
        match choice:
            case 1:
                menu_product()
            case 2:
                menu_manager()
            case 3:
                menu_buyer()
            case 4:
                break


def menu_product():
    '''Меню редагування товарів'''
    while True:
        choice = int(input("""
                    1. Додати товар
                    2. Додати кількість товару
                    3. Редагувати товар
                    4. Вивести список товарів
                    5. Вихід
                    """))
        match choice:
            case 1:
                add_products()
            case 2:
                add_quantity_product()
            case 3:
                product_id = int(input('Enter the ID-product: '))
                product_name = input('Enter new name of product: ')
                change_product(product_id, product_name)
            case 4:
                display_all_products()
            case 5:
                break


def menu_manager():
    '''Меню редагування продавців'''
    while True:
        choice = int(input("""
                       1. Додати продавця (менеджера)
                       2. Редагувати продавця
                       3. Вивести список продавців
                       4. Вихід
                       """))
        match choice:
            case 1:
                add_manager()
            case 2:
                manager_id = int(input('Enter the ID-manager: '))
                manager_name = input('Enter new name of manager: ')
                change_manager(manager_id, manager_name)
            case 3:
                display_all_managers()
            case 4:
                break


def menu_buyer():
    '''Меню редагування продавців'''
    while True:
        choice = int(input("""
                       1. Додати покупця
                       2. Редагувати покупця
                       3. Вивести список покупців
                       4. Вихід
                       """))
        match choice:
            case 1:
                add_buyer()
            case 2:
                buyer_id = int(input('Enter the ID-buyer: '))
                buyer_name = input('Enter new name of buyer: ')
                change_buyer(buyer_id, buyer_name)
            case 3:
                display_all_buyers()
            case 4:
                break


def menu_orders():
    while True:
        choice = int(input("""
                1. Створити замовлення
                2. Вивести список замовлень
                3. Вивести замовлення за номером
                4. Вихід
                """))
        match choice:
            case 1:
                # вибрати покупця
                display_all_buyers()
                buyer_id = int(input('Enter id-buyer: '))
                # вибрати менеджера
                display_all_managers()
                manager_id = int(input('Enter id-manager: '))
                # вивести список товару
                display_all_products()
                create_order(session, buyer_id, manager_id)
            case 2:
                display_all_orders(session)
            case 3:
                order_id = int(input('Enter the id-order: '))
                display_orders_id(order_id)
            case 4:
                session.close()
                break


def main():
    # Base.metadata.drop_all(engine)  # Удалит все таблицы
    # Base.metadata.create_all(engine)  # Пересоздаст

    while True:
        choice = int(input("""
                1. Словники
                2. Замовлення
                3. Вихід
                """))
        match choice:
            case 1:
                menu_editing_data()
            case 2:
                menu_orders()
            case 3:
                session.close()
                break


main()
