from dataclasses import dataclass

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


@dataclass
class Customer(Base):
    __tablename__ = 'customers'

    id: int
    name: str
    email: str
    date: str

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    date = Column(String)

    cars = relationship('Car', back_populates='customer')


@dataclass
class Car(Base):
    __tablename__ = 'cars'

    id: int
    model: str
    condition: str
    price: str
    customer_id: int

    id = Column(Integer, primary_key=True)
    model = Column(String)
    condition = Column(String)
    price = Column(Integer)

    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship('Customer', back_populates='cars')


def main():
    pass


if __name__ == '__main__':
    main()
