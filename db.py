from sqlalchemy import create_engine, Column, INTEGER, VARCHAR, DATE, NUMERIC, ForeignKey, BOOLEAN, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DIALECT = "postgresql"
DRIVER = "psycopg2"
USERNAME = "postgres"
PASSWORD = "postgres"
HOST = "localhost"
PORT = "5432"
DATABASE = "sales-db"

engine = create_engine(
    f"{DIALECT}+{DRIVER}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

Base = declarative_base()


class Client(Base):
    __tablename__ = "client-tb"
    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(length=255), nullable=False)
    birth_date = Column(DATE, nullable=False)

    def __repr__(self):
        return f"Client(id={self.id}, name={self.name}, birth_date={self.birth_date})"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'birth_date': self.birth_date
        }


class Product(Base):
    __tablename__ = "product-tb"
    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(length=255), nullable=False)
    price = Column(NUMERIC(precision=8, scale=2), nullable=False)
    inventory = Column(INTEGER, default=0, nullable=False)

    def __repr__(self):
        return f"Product(id={self.id}, name={self.name}, price={self.price}, inventory={self.inventory})"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'inventory': self.inventory
        }


class ShoppingCart(Base):
    __tablename__ = "shopping-cart-tb"
    id = Column(INTEGER, primary_key=True)
    sale_id = Column(INTEGER, ForeignKey("sale-tb.id"), nullable=False)
    product_id = Column(INTEGER, ForeignKey("product-tb.id"), nullable=False)
    quantity = Column(INTEGER, default=1, nullable=False)
    sub_total_price = Column(NUMERIC(precision=8, scale=2))

    def __repr__(self):
        return f"ShoppingCart(id={self.id}, client_id={self.client_id}, product_id={self.product_id}, " \
               f"quantity={self.quantity} sub_total_price={self.sub_total_price})"

    def to_dict(self):
        return {
            'id': self.id,
            'sale_id': self.sale_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'sub_total_price': self.sub_total_price
        }


class Sale(Base):
    __tablename__ = "sale-tb"
    id = Column(INTEGER, primary_key=True)
    client_id = Column(INTEGER, ForeignKey("client-tb.id"), nullable=False)
    sale_date = Column(TIMESTAMP(timezone=True), nullable=False)
    total_price = Column(NUMERIC(precision=8, scale=2))
    is_paid = Column(BOOLEAN, default=False, nullable=False)

    def __repr__(self):
        return f"Sale(id={self.id}, client_id={self.client_id},  sale_date={self.sale_date}, " \
               f"total_price={self.total_price}, is_paid={self.is_paid})"

    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'sale_date': self.sale_date,
            'total_price': self.total_price,
            'is_paid': self.is_paid
        }


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
