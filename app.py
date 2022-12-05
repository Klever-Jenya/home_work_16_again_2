import json

from flask import request, Flask
from flask_sqlalchemy import SQLAlchemy

from main import User, Order, Offer, init_database

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///homework16_again.db"  #:memory:
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # отключить

db = SQLAlchemy(app)  # связь базы данных с приложением


# --------------------Users-----------------
# ---------соединяя 2-3 метода в одной вьюшке------------
@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        result = []
        for u in User.query.all():
            result.append(u.do_dict())

        return json.dumps(result), 200

    if request.method == "POST":
        user_data = json.loads(request.data)
        new_user = User(
            id=user_data["id"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            age=user_data["age"],
            email=user_data["email"],
            role=user_data["role"],
            phone=user_data["phone"]
        )

        db.session.add(new_user)
        db.session.commit()

        return "Пользователь добавлен", 201  # на создание


@app.route("/users/<int:uid>", methods=["GET", "PUT", "DELETE"])
def user(uid: int):
    if request.method == "GET":  # берем юзера по id
        return json.dumps(User.query.get(uid).do_dict()), 200

    if request.method == "PUT":
        user_data = json.loads(request.data)
        u = User.query.get(uid)
        # id PUTом изменить не получиться
        u.first_name = user_data["first_name"],
        u.last_name = user_data["last_name"],
        u.age = user_data["age"],
        u.email = user_data["email"],
        u.role = user_data["role"],
        u.phone = user_data["phone"]

        db.session.add(u)
        db.session.commit()
        return "Пользователь изменен", 204  # обновление

    if request.method == "DELETE":
        u = User.query.get(uid)

        db.session.delete(u)
        db.session.commit()

        return "Пользователь удален", 204  # обновление


# --------------------Orders-----------------

@app.route("/orders", methods=["GET", "POST"])
def orders():
    if request.method == "GET":
        result = []
        for u in Order.query.all():
            result.append(u.do_dict())

        return json.dumps(result), 200

    if request.method == "POST":
        order_data = json.loads(request.data)
        new_order = Order(
            id=order_data["id"],
            name=order_data["name"],
            description=order_data["description"],
            start_date=order_data["start_date"],
            end_date=order_data["end_date"],
            address=order_data["address"],
            price=order_data["price"],
            customer_id=order_data["customer_id"],
            executor_id=order_data["executor_id"]
        )

        db.session.add(new_order)
        db.session.commit()

        return "Заказ добавлен", 201  # на создание


@app.route("/orders/<int:uid>", methods=["GET", "PUT", "DELETE"])
def order(uid: int):
    if request.method == "GET":  # берем юзера по id
        return json.dumps(Order.query.get(uid).do_dict()), 200

    if request.method == "PUT":
        order_data = json.loads(request.data)
        u = Order.query.get(uid)
        # id PUTом изменить не получиться
        u.name = order_data["name"],
        u.description = order_data["description"],
        u.start_date = order_data["start_date"],
        u.end_date = order_data["end_date"],
        u.address = order_data["address"],
        u.price = order_data["price"],
        u.customer_id = order_data["customer_id"],
        u.executor_id = order_data["executor_id"]

        db.session.add(u)
        db.session.commit()
        return "Заказ изменен", 204  # обновление

    if request.method == "DELETE":
        u = Order.query.get(uid)

        db.session.delete(u)
        db.session.commit()

        return "Заказ удален", 204  # обновление


# --------------------Offers-----------------

@app.route("/offers", methods=["GET", "POST"])
def offers():
    if request.method == "GET":
        result = []
        for u in Offer.query.all():
            result.append(u.do_dict())

        return json.dumps(result), 200

    if request.method == "POST":
        offer_data = json.loads(request.data)
        new_offer = Offer(
            id=offer_data["id"],
            order_id=offer_data["order_id"],
            executor_id=offer_data["executor_id"]
        )

        db.session.add(new_offer)
        db.session.commit()

        return "Выполнение заказа добавлено", 201  # на создание


@app.route("/offers/<int:uid>", methods=["GET", "PUT", "DELETE"])
def offer(uid: int):
    if request.method == "GET":  # берем юзера по id
        return json.dumps(Offer.query.get(uid).do_dict()), 200

    if request.method == "PUT":
        offer_data = json.loads(request.data)
        u = Offer.query.get(uid)
        # id PUTом изменить не получиться
        u.order_id = offer_data["order_id"],
        u.executor_id = offer_data["executor_id"]

        db.session.add(u)
        db.session.commit()
        return "Выполнение заказа изменено", 204  # обновление

    if request.method == "DELETE":
        u = Offer.query.get(uid)

        db.session.delete(u)
        db.session.commit()

        return "Выполнение заказа удалено", 204  # обновление


if __name__ == '__main__':
    init_database()
    app.run(debug=True)