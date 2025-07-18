from buyer_service import display_all_buyers
from manager_service import display_all_managers
from models import Order, Manager, Buyer, OrderProduct, Product
from product_service import display_all_products


def menu_orders(session):
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
                display_all_buyers(session)
                buyer_id = int(input('Enter id-buyer: '))
                # вибрати менеджера
                display_all_managers(session)
                manager_id = int(input('Enter id-manager: '))
                # вивести список товару
                display_all_products(session)
                create_order(session, buyer_id, manager_id)
            case 2:
                display_all_orders(session)
            case 3:
                order_id = int(input('Enter the id-order: '))
                display_order_on_id(session, order_id)
            case 4:
                session.close()
                break


def add_product():
    # вказати id-товару, та кількість
    product_id = int(input("Enter id-product: "))
    quantity = int(input("Enter quantity product: "))
    return product_id, quantity


def save_order(session, manager_id, buyer_id, list_products):
    try:
        # заповнити таблицю orders
        # Получаем существующих менеджера и покупателя
        manager = session.query(Manager).get(manager_id)
        buyer = session.query(Buyer).get(buyer_id)

        order = Order(manager=manager, buyer=buyer)
        session.add(order)
        session.commit()

        # заповнити таблицю order_product
        for product_id, amount in list_products:
            # print(product, amount)
            product = session.query(Product).get(product_id)
            order_product = OrderProduct(order=order, product=product, quantity=amount)
            session.add(order_product)

        session.commit()
        print(f'Замовлення id-{order.id} створено')
        # return session.refresh(order)
    finally:
        session.close()


def create_order(session, buyer_id, manager_id):
    print('create_order')
    list_products = [add_product()]
    while True:
        choice = int(input('1-Додати 2-Зберегти 3-Вийти'))
        match choice:
            case 1:
                list_products.append(add_product())
            case 2:
                save_order(session, manager_id, buyer_id, list_products)
                break
            case 3:
                break


def display_all_orders(session):
    try:
        orders = session.query(
            Order.id,
            Manager.name.label("manager_name"),
            Buyer.name.label("buyer_name")
        ).join(Order.manager).join(Order.buyer).all()

        for order in orders:
            print(f'{order.id} - {order.manager_name} - {order.buyer_name}')
    finally:
        session.close()


def display_order_on_id(session, order_id):
    try:
        order_products = session.query(OrderProduct).filter_by(order_id=order_id).all()
        order = session.query(Order).get(order_id)
        buyer = session.query(Buyer).get(order.buyer_id)
        manager = session.query(Manager).get(order.manager_id)
        text = f"""
                Замовлення N {order.id}
            Покупець: {buyer.name}       Продавець: {manager.name}
        """
        ind = 0

        for op in order_products:
            ind += 1
            product = session.query(Product).get(op.product_id)
            text += f"\n\t\t{ind}. {product.name} - {op.quantity} шт."
        print(text)
    finally:
        session.close()
