import json
import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import *

"""Вьюшки для Orders, Users и Offers"""

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
            return "Пользователь не найден", 404
        else:
            return jsonify(user.to_dict())
    elif request.method == 'PUT':
        user_data = json.loads(request.data)
        user = db.session.query(User).get(user_id)
        if user is None:
            return "Пользователь не найден", 404
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.age = user_data['age']
        user.email = user_data['email']
        user.role = user_data['role']
        user.phone = user_data['phone']
        db.session.add(user)
        db.session.commit()
        db.session.close()
        return f"Пользователь с id {user_id} успешно изменён!", 200
    elif request.method == 'DELETE':
        user = db.session.query(User).get(user_id)
        if user is None:
            return "Пользователь не найден", 404
        db.session.delete(user)
        db.session.commit()
        db.session.close()
        return f"Пользователь с id {user_id} успешно удалён!", 200


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
            return repr(error), 500


@app.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def one_order(order_id):
    if request.method == 'GET':
        order = db.session.query(Order).get(order_id)
        if order is None:
            return "Заказ не найден"
        else:
            return jsonify(order.to_dict())

    elif request.method == 'PUT':
        order_data = json.loads(request.data)
        order = db.session.query(Order).get(order_id)
        if order is None:
            return "Заказ не найден", 404

        month_start, day_start, years_start = [int(order_date) for order_date in order_data['start_date'].split("/")]
        month_end, day_end, years_end = [int(order_date) for order_date in order_data['end_date'].split("/")]

        order.name = order_data['name']
        order.description = order_data['description']
        order.start_date = datetime.date(month=month_start, day=day_start, year=years_start)
        order.end_date = datetime.date(month=month_end, day=day_end, year=years_end)
        order.address = order_data['address']
        order.price = order_data['price']
        order.customer_id = order_data['customer_id']
        order.executor_id = order_data['executor_id']
        db.session.add(order)
        db.session.commit()
        db.session.close()
        return f"Заказ с id {order_id} успешно изменён!", 200

    elif request.method == 'DELETE':
        order = db.session.query(Order).get(order_id)
        if order is None:
            return "Заказ не найден", 404
        db.session.delete(order)
        db.session.commit()
        db.session.close()
        return f"Заказ с id {order_id} успешно удалён!", 200


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
    elif request.method == 'PUT':
        offer_data = json.loads(request.data)
        offer = db.session.query(Offer).get(offer_id)
        if offer is None:
            return "Предложение не найдено", 404
        offer.order_id = offer_data['order_id']
        offer.executor_id = offer_data['executor_id']
        db.session.add(offer)
        db.session.commit()
        db.session.close()
        return f"Предложение с id {offer_id} успешно изменено!", 200
    elif request.method == 'DELETE':
        offer = db.session.query(Offer).get(offer_id)
        if offer is None:
            return "Предложение не найдено", 404
        db.session.delete(offer)
        db.session.commit()
        db.session.close()
        return f"Предложение с id {offer_id} успешно удалено!", 200


if __name__ == '__main__':
    app.run(debug=True, port=1608)
