import json
import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///hw_base.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        result = []
        for user in db.session.query(User).all():
            result.append(user.to_dict())
        return jsonify(result)
    if request.method == 'POST':
        try:
            new_user = json.loads(request.data)
            new_user_obj = User(
                id=new_user['id'],
                first_name=new_user['first_name'],
                last_name=new_user['last_name'],
                age=new_user['age'],
                email=new_user['email'],
                role=new_user['role'],
                phone=new_user['phone']
            )
            db.session.add(new_user_obj)
            db.session.commit()
            db.session.close()
            return "Пользователь создан в базе данных", 200
        except Exception as error:
            return error


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def one_user(user_id):
    if request.method == 'GET':
        user = db.session.query(User).get(user_id)
        if user is None:
            return "Пользователь не найден"
        else:
            return jsonify(user.to_dict())


@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'GET':
        result = []
        for order in db.session.query(Order).all():
            result.append(order.to_dict())
        return jsonify(result)
    if request.method == 'POST':
        try:
            new_order = json.loads(request.data)
            month_start, day_start, years_start = new_order['start_date'].split("/")
            month_end, day_end, years_end = new_order['end_date'].split("/")
            new_order_obj = Order(
                id=new_order['id'],
                name=new_order['name'],
                description=new_order['description'],
                start_date=datetime.date(month=int(month_start), day=int(day_start), year=int(years_start)),
                end_date=datetime.date(month=int(month_end), day=int(day_end), year=int(years_end)),
                address=new_order['address'],
                price=new_order['price'],
                customer_id=new_order['customer_id'],
                executor_id=new_order['executor_id']
            )
            db.session.add(new_order_obj)
            db.session.commit()
            db.session.close()
            return "Заказ создан в базе данных", 200
        except Exception as error:
            return error


@app.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def one_order(order_id):
    if request.method == 'GET':
        order = db.session.query(Order).get(order_id)
        if order is None:
            return "Заказ не найден"
        else:
            return jsonify(order.to_dict())


@app.route('/offers', methods=['GET', 'POST'])
def offers():
    if request.method == 'GET':
        result = []
        for offer in db.session.query(Offer).all():
            result.append(offer.to_dict())
        return jsonify(result)
    if request.method == 'POST':
        try:
            new_offer = json.loads(request.data)
            new_offer_obj = Offer(
                id=new_offer['id'],
                order_id=new_offer['order_id'],
                executor_id=new_offer['executor_id']
            )
            db.session.add(new_offer_obj)
            db.session.commit()
            db.session.close()
            return "Предложение создано в базе данных", 200
        except Exception as error:
            return error


@app.route('/offers/<int:offer_id>', methods=['GET', 'PUT', 'DELETE'])
def one_offer(offer_id):
    if request.method == 'GET':
        offer = db.session.query(Offer).get(offer_id)
        if offer is None:
            return "Предложение не найдено"
        else:
            return jsonify(offer.to_dict())


if __name__ == '__main__':
    app.run(debug=True, port=1608)
