import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json

from models_hw import create_tables, Publisher, Book, Shop, Stock, Sale

login = input('Введите логин для подключения к БД\n')
password = input('Введите пароль для подключения к БД\n')
name_db = input('Введите название БД, к которой вы хотите подключиться\n')

DSN = f'postgresql://{login}:{password}@localhost:5432/{name_db}'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()




while True:
    name_or_id = input('Введите имя или идентификатор издателя: \n')
    try:
        id = int(name_or_id)
        subq_q = session.query(Publisher).filter(Publisher.id == id).subquery('publisher_id')

    except Exception:
        name = name_or_id
        subq_q = session.query(Publisher).filter(Publisher.name.like(name)).subquery('publisher_id')
    books_q = session.query(Book).join(subq_q, Book.id_publisher == subq_q.c.id)
    for book in books_q.all():
        book_name = book.title
        book_id = book.id
        q_stock = session.query(Stock).filter(Stock.id_book == book_id)
        for stock in q_stock.all():
            shop_id = stock.id_shop
            q_shop = session.query(Shop).filter(Shop.id == shop_id)
            shop = q_shop.all()[0]
            shop_name = shop.name
            q_sale = session.query(Sale).filter(Sale.id_stock == stock.id)
            for sale in q_sale.all():
                price = sale.price
                date = sale.date_sale
            print(f'{book_name} | {shop_name} | {price} | {date}')


session.close()