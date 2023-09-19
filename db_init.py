import datetime

"""Создание БД"""


from app import *
from models import *
from config import *

with app.app_context():
    db.drop_all()
    db.create_all()

    for user in users:
        db.session.add(User(
            id=user['id'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            age=user['age'],
            email=user['email'],
            role=user['role'],
            phone=user['phone']
        ))
        db.session.commit()
        db.session.close()

    for order in orders:
        month_start, day_start, years_start = order['start_date'].split("/")
        month_end, day_end, years_end = order['end_date'].split("/")

        db.session.add(Order(
            id=order['id'],
            name=order['name'],
            description=order['description'],
            start_date=datetime.date(month=int(month_start), day=int(day_start), year=int(years_start)),
            end_date=datetime.date(month=int(month_end), day=int(day_end), year=int(years_end)),
            address=order['address'],
            price=order['price'],
            customer_id=order['customer_id'],
            executor_id=order['executor_id']
        ))
        db.session.commit()
        db.session.close()

    for offer in offers:
        db.session.add(Offer(
            id=offer['id'],
            order_id=offer['order_id'],
            executor_id=offer['executor_id']
        ))
        db.session.commit()
        db.session.close()
