import json

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///hw_base.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        result = []
        for user in db.session.query(User).all():
            result.append(user.to_dict())
        return jsonify(result)


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
