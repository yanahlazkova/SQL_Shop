''' Функції роботи з таблицею товарів (додавання, видалення, оновлення...'''
import fakerdata as fake
from models import Product, ProductMovement


def menu_product(session):
    '''Меню редагування товарів'''
    while True:
        choice = int(input("""
                    1. Додати товар
                    2. Додати кількість товару
                    3. Редагувати товар
                    4. Вивести залишки товарів
                    5. Вихід
                    """))
        match choice:
            case 1:
                add_products(session)
            case 2:
                incoming_product(session)
            case 3:
                product_id = int(input('Enter the ID-product: '))
                product_name = input('Enter new name of product: ')
                change_product(session, product_id, product_name)
            case 4:
                display_all_products(session)
            case 5:
                break


def add_products(session):
    try:
        for _ in range(12):
            product = Product(name=fake.get_product())
            session.add(product)
            session.commit()
            session.refresh(product)
            print(f'{product.id} - {product.name} додано.')
    finally:
        session.close()


def incoming_product(session):
    """надходження товару"""
    try:
        display_all_products(session)
        product_id = int(input(f'Вкажіть ID товару: '))

        product = session.query(Product).get(product_id)

        count_product = int(input(f'Введіть кількість {product.name}: '))

        product_incoming = ProductMovement(product=product, quantity=count_product)
        session.add(product_incoming)
        session.commit()
        session.refresh(product_incoming)
        print(f'Додано надходження:\n'
              f'{product_incoming.id} - {product_incoming.product.name} - {product_incoming.quantity}')
    finally:
        session.close()



def change_product(session, product_id, name):
    """Змінити назву товару"""
    try:
        product = session.query(Product).filter_by(id=product_id).first()
        product.name = name
        session.commit()
        session.refresh(product)
        print(f'{product.id} - {product.name} оновлено.')
    finally:
        session.close()


def display_all_products(session):
    """Вивести список всіх товарів"""
    try:
        products = session.query(Product.id, Product.name)
        print("""
                СПИСОК ТОВАРІВ:
        """)
        text = ''
        for product_id, product_name in products:
            text += f'\n\t\t{product_id}. {product_name}'
        print(text)
    finally:
        session.close()

