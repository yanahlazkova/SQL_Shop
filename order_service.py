from models import Order, Manager, Buyer, OrderProduct, Product


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


def display_orders_id(session, order_id):
    products = session.query(OrderProduct.product_id).filter_in(Order.id == order_id).all()
    for product in products:
        print(product)