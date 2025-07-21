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
    product = random.choice(tech_items)
    return product


def get_random_number():
    # return fake.random_int(min=-1000, max=1000, step=10)
    return fake.random_int(max=300, step=10)


