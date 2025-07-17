from faker import Faker
import random


fake = Faker('uk-UA')

def get_person_name():
    return fake.name()

def get_email():
    return fake.email()


tech_items = [
        "Ноутбук Lenovo ThinkPad", "Монитор Samsung 27''", "Мышь Logitech MX Master 3",
        "Клавиатура HyperX Alloy", "Видеокарта RTX 4060", "SSD Kingston 1TB",
        "Оперативная память Corsair 16GB", "Материнская плата ASUS", "Корпус Zalman",
        "Блок питания Chieftec", "Веб-камера Logitech C920", "Наушники SteelSeries Arctis"
    ]


def get_product():
    return random.choice(tech_items)


