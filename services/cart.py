from sqlalchemy.exc import NoResultFound

from db import session, Product, Sale


def sum_sub_total_price(product_id, quantity):
    try:
        product = session.query(Product).filter(Product.id == product_id).one()
        return product.price * quantity
    except NoResultFound:
        raise NoResultFound('Product not found')

def decrease_stock(product_id, quantity):
    try:
        product = session.query(Product).filter(Product.id == product_id).one()
        product.inventory -= quantity
        if product.inventory < 0:
            raise Exception('Stock is not enough')
        session.commit()
    except NoResultFound:
        raise NoResultFound('Product not found')

def increase_stock(product_id, quantity):
    try:
        product = session.query(Product).filter(Product.id == product_id).one()
        product.inventory += quantity
        session.commit()
    except NoResultFound:
        raise NoResultFound('Product not found')

def decrease_total_price(sale_id, sub_total_price):
    try:
        sale = session.query(Sale).filter(Sale.id == sale_id).one()
        sale.total_price -= sub_total_price
        session.commit()
    except NoResultFound:
        raise NoResultFound('Sale not found')

def increase_total_price(sale_id, sub_total_price):
    try:
        sale = session.query(Sale).filter(Sale.id == sale_id).one()
        sale.total_price += sub_total_price
        session.commit()
    except NoResultFound:
        raise NoResultFound('Sale not found')