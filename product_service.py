''' Функції роботи з таблицею товарів (додавання, видалення, оновлення...'''
import fakerdata as fake
from models import Product, ProductMovement
from sqlalchemy import func


def menu_product(session):
    '''Меню редагування товарів'''
    while True:
        choice = int(input("""
                    1. Додати товар
                    2. Додати кількість товару
                    3. Редагувати товар
                    4. Вивести залишки товарів
                    5. Ввести залишки товаів
                    6. Вихід
                    """))
        match choice:
            case 1:
                add_products(session)
            case 2:
                display_all_products(session)
                product_id = int(input(f'Вкажіть ID товару: '))
                count_product = int(input(f'Введіть кількість: '))

                incoming_product(product_id, count_product, session)

            case 3:
                product_id = int(input('Enter the ID-product: '))
                product_name = input('Enter new name of product: ')
                change_product(session, product_id, product_name)
            case 4:
                # display_all_products(session)
                display_balance_products(session)
            case 5:
                # Заповнення таблиці ProductMovement(надходження або вибуття товарів)
                add_balance(session)
            case 6:
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


def incoming_product(product_id, count_product, session):
    """надходження товару"""
    try:
        product = session.query(Product).get(product_id)
        product_incoming = ProductMovement(product=product, quantity=count_product)
        session.add(product_incoming)
        session.commit()
        session.refresh(product_incoming)
        print(f'Додано надходження:\n'
              f'{product_incoming.id} - {product_incoming.product.name} - {product_incoming.quantity}')
    finally:
        session.close()


def outgoing_product(product_id, count, session):
    """зменшення кількості товару"""
    try:
        # отримаємо загальну кількість товару
        result = (session.query(func.sum(ProductMovement.quantity))
                  .filter(ProductMovement.product_id == product_id).scalar())
        print(f'Загальна кількість товару на складі {result} шт.')

        if result >= count:
            incoming_product(product_id, (count * (-1)), session)
        else:
            print(f'Недестатня кількість товару{(session.query(Product).get(product_id)).name}: {result}шт.')

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


def display_balance_products(session):
    try:
        # products_balance = (session.query(ProductMovement.product_id,
        #                                   func.sum(ProductMovement.quantity)
        #                                   .label('stock'))
        #                     .group_by(ProductMovement.product_id).all())
        # products_balance = (
            # session.query(Product.name, func.sum(ProductMovement.quantity).label('stock'))
            # .join(Product).group_by(Product.name).all())

        products_balance = (session.query(Product.name, func.sum(ProductMovement.quantity).label('stock'))
            .join(Product)
            .group_by(Product.id)
            .having(func.sum(ProductMovement.quantity) != 0)
            .all()
                            )
        text = '''
                        ЗАЛИШКИ ТОВАРІВ:
        \n'''
        if products_balance:
            i = 0
            for product, stock in products_balance:
                i += 1
                # product = session.query(Product).get(product_id)
                text += f'\t\t{i}. {product}\tзалишок: {stock}\n'
            print(text)
        else:
            print('Немає залків, склад порожній...')
    finally:
        session.close()


def add_balance(session):
    """"Проходить по кожному товару з табл.Product
    та виконує надходження"""
    try:
        # """Додавання кількості товару вручну"""
        # products = session.query(Product.id, Product.name)
        # list_products = []
        # for product_id, product in products:
        #     list_products.append({
        #         'id': product_id,
        #         'name': product,
        #         'count': 0
        #     })
        #
        # for product in list_products:
        #     # product['count'] = int(input(f'Enter balance {product['name']}: '))
        #     product['count'] = fake.get_random_number()
        #     print(product)
        """Додавання рандомно кількості товару """
        products = session.query(Product)
        # for product_id in products:
        #     incoming_product(product_id, fake.get_random_number(), session)
        for product in products:
            # print(product.id)
            product_movement = ProductMovement(product_id=product.id, quantity=fake.get_random_number())
            session.add(product_movement)
            session.commit()

    finally:
        session.close()