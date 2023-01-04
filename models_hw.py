import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()



class Publisher(Base):
    __tablename__ = 'publisher'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=100), unique=True)

class Book(Base):
    __tablename__ = 'book'
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=100), unique=True)
    id_publisher=sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)
    publisher = relationship(Publisher, backref='books')

class Shop(Base):
    __tablename__ = 'shop'
    id = sq.Column(sq.Integer, primary_key=True, unique=True)
    name = sq.Column(sq.String, unique=True, nullable=False)

class Stock(Base):
    __tablename__ = 'stock'
    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer)

    shop = relationship(Shop, backref='stocks')
    book = relationship(Book, backref='stocks')



class Sale(Base):
    __tablename__ = 'sale'
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.DateTime)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'))
    count = sq.Column(sq.Integer)

    stock = relationship(Stock, backref='sales')

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
