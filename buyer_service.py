from models import Buyer, Email
import fakerdata as fake


def menu_buyer(session):
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
                add_buyer(session)
            case 2:
                buyer_id = int(input('Enter the ID-buyer: '))
                buyer_name = input('Enter new name of buyer: ')
                change_buyer(session, buyer_id, buyer_name)
            case 3:
                display_all_buyers(session)
            case 4:
                break


def add_buyer(session):
    try:
        buyer = Buyer(name=fake.get_person_name())
        buyer.email = Email(email=fake.get_email())
        session.add(buyer)
        session.commit()
        session.refresh(buyer)
        print(f'Buyer added: {buyer.id} - {buyer.name} - {buyer.email.email}.')
    finally:
        session.close()


def change_buyer(session, buyer_id, name):
    """Змінити назву товару"""
    try:
        buyer = session.query(Buyer).filter_by(id=buyer_id).first()
        buyer.name = name
        session.commit()
        session.refresh(buyer)
        print(f'Дані покупця {buyer.id} - {buyer.name} оновлено.')
    finally:
        session.close()


def display_all_buyers(session):
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

