''' Функції роботи з таблицею товарів (додавання, видалення, оновлення...'''
import fakerdata as fake
from models import Manager


def menu_manager(session):
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
                add_manager(session)
            case 2:
                manager_id = int(input('Enter the ID-manager: '))
                manager_name = input('Enter new name of manager: ')
                change_manager(session, manager_id, manager_name)
            case 3:
                display_all_managers(session)
            case 4:
                break


def add_manager(session):
    try:
        manager = Manager(name=fake.get_person_name())
        session.add(manager)
        session.commit()
        session.refresh(manager)
        print(f'Manager added: - {manager.id} - {manager.name}.')
    finally:
        session.close()


def change_manager(session, manager_id, name):
    """Змінити назву товару"""
    try:
        manager = session.query(Manager).filter_by(id=manager_id).first()
        manager.name = name
        session.commit()
        session.refresh(manager)
        print(f'Дані продавця {manager.id} - {manager.name} оновлено.')
    finally:
        session.close()


def display_all_managers(session):
    """Вивести список всіх товарів"""
    try:
        managers = session.query(Manager.id, Manager.name)
        for manager_id, manager_name in managers:
            print(manager_id, manager_name)
    finally:
        session.close()

