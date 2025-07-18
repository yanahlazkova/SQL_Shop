import os

import buyer_service
import manager_service
import order_service
import product_service
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

if __name__ == '__main__':
    Base.metadata.create_all(engine)

session = get_session()



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
                product_service.menu_product(session)
            case 2:
                manager_service.menu_manager(session)
            case 3:
                buyer_service.menu_buyer(session)
            case 4:
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
                order_service.menu_orders(session)
            case 3:
                session.close()
                break


main()
