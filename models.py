from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Buyer(Base):
    __tablename__ = 'buyers'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email_id = Column(Integer, ForeignKey('emails.id'), nullable=False)

    email = relationship("Email", back_populates="buyer")
    orders = relationship("Order", back_populates="buyer")


class Email(Base):
    __tablename__ = 'emails'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    # buyer_id = Column(Integer, ForeignKey('buyers.id'), nullable=False)
#
    buyer = relationship('Buyer', back_populates='email', uselist=False)


class Manager(Base):
    __tablename__ = 'managers'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))


class Order(Base):
    '''У замовлення може бути один покупець і один продавець'''
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    number = Column(Integer, unique=True, nullable=False)
    manager_id = Column(Integer, ForeignKey('managers.id'), nullable=False)
    buyer_id = Column(Integer, ForeignKey('buyers.id'), nullable=False)

    manager = relationship('Manager', back_populates='order')
    buyer = relationship('Buyer', back_populates='order')

    order_products = relationship("OrderProduct", back_populates='order')
    products = relationship('Product', secondary='order_product', viewonly=True)



class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    order_products = relationship('OrderProduct', back_populates='product')
    orders = relationship('Order', secondary='order_product')


class OrderProduct(Base):
    __tablename__ = 'order_product'

    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    quantity = Column(Integer, nullable=False, default=1)

    order = relationship('Order', back_populates='order_product')
    product = relationship('Product', back_populates='order_product')
