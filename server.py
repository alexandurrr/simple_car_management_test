from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from controllers.customers_cars import Customer, Car, CustomerList, CarList
from services.customers_cars import CustomerService, CarService


def main():
    # Create the Flask app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rental.sqlite'

    # Create the Flask-RESTful API
    api = Api(app)

    # Connect to the database with Flask-SQLAlchemy
    db = SQLAlchemy(app)

    customers = CustomerService(db)

    # Register the route for each resource
    api.add_resource(CustomerList, '/customers/',
                     resource_class_args=[customers])

    api.add_resource(Customer, '/customers/<id>',
                     resource_class_args=[customers])
    cars = CarService(db)

    # Register the route for each resource
    api.add_resource(CarList, '/cars/',
                     resource_class_args=[cars])

    api.add_resource(Car, '/cars/<id>',
                     resource_class_args=[cars])
    app.run(debug=True)


if __name__ == '__main__':
    main()