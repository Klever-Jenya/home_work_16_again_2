from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import raw_data

# from sqlalchemy.orm import relationship

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///homework16_again.db"  #:memory:
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # отключить

db = SQLAlchemy(app)  # связь базы данных с приложением


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String)
    role = db.Column(db.String)  # должность
    phone = db.Column(db.String)

    def do_dict(self):  # питонячий формат
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone
        }


class Order(db.Model):  # заказ
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)  # описание
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # покупатель
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # исполнитель


    def do_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id
        }


class Offer(db.Model):  # Предложение/ скидка
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # исполнитель
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))  # номер заказа

    def do_dict(self):
        return {
            "id": self.id,
            "executor_id": self.executor_id,
            "order_id": self.order_id
        }


def init_database():
    db.drop_all()  # очистить
    db.create_all()  # залить

    for user_data in raw_data.users:  # если не переделывать данные в JSON формат
        new_user = User(
            id=user_data["id"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            age=user_data["age"],
            email=user_data["email"],
            role=user_data["role"],
            phone=user_data["phone"]
        )

        db.session.add(new_user)  # добавляем в базу данных
        db.session.commit()  # делаем коммит

    for order_data in raw_data.orders:
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

    for offer_data in raw_data.offers:
        new_offer = Offer(
            id=offer_data['id'],
            executor_id=offer_data['executor_id'],
            order_id=offer_data['order_id']
        )

        db.session.add(new_offer)
        db.session.commit()



