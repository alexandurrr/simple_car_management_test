from flask import jsonify, make_response, request
from flask_restful import Resource
from werkzeug.exceptions import *


# Class responsible for /customers/
class CustomerList(Resource):
    def __init__(self, customers):
        self.customers = customers

    def get(self):
        return jsonify(self.customers.get_all())

    def post(self):
        customer = self.customers.add(request.json)

        return make_response(jsonify(customer), 201)


# Class responsible for /cars/
class CarList(Resource):
    def __init__(self, cars):
        self.cars = cars

    def get(self):
        return jsonify(self.cars.get_all())

    def post(self):
        car = self.cars.add(request.json)

        return make_response(jsonify(car), 201)


# Class responsible for /customers/<id>
class Customer(Resource):
    def __init__(self, customers):
        self.customers = customers

    def get(self, id):
        customer = self.customers.get(id)

        if not customer:
            raise NotFound('Invalid id, customer not found.')

        return jsonify(customer)

    def put(self, id):
        customer = self.customers.get(id)

        if not customer:
            raise NotFound('Invalid id, customer not found.')

        json = request.get_json()

        customer.name = json['name']
        customer.email = json['email']
        customer.date = json['date']

        self.customers.update(customer)

        return jsonify(customer)

    def delete(self, id):
        customer = self.customers.get(id)

        if not customer:
            raise NotFound('Invalid id, customer not found.')

        self.customers.delete(customer)

        return jsonify(customer)


class Car(Resource):
    def __init__(self, cars):
        self.cars = cars

    def get(self, id):
        car = self.cars.get(id)

        if not car:
            raise NotFound('Invalid id, car not found.')

        return jsonify(car)

    def put(self, id):
        car = self.cars.get(id)

        if not car:
            raise NotFound('Invalid id, car not found.')

        json = request.get_json()

        car.model = json['model']
        car.condition = json['condition']
        car.price = json['price']

        self.cars.update(car)

        return jsonify(car)

    def delete(self, id):
        car = self.cars.get(id)

        if not car:
            raise NotFound('Invalid id, car not found.')

        self.cars.delete(car)

        return jsonify(car)
