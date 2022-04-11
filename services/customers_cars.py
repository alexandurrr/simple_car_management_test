from model.customer_car import Customer, Car


class CustomerService:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        return self.db.session.query(Customer).all()

    def get(self, id):
        return self.db.session.query(Customer).get(id)

    def add(self, json):
        customer = Customer(name=json['name'], email=json['email'], date=json['date'])

        self.db.session.add(customer)
        self.db.session.commit()

        return customer

    def update(self, customer):
        self.db.session.commit()

    def delete(self, customer):
        self.db.session.delete(customer)
        self.db.session.commit()


class CarService:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        return self.db.session.query(Car).all()

    def get(self, id):
        return self.db.session.query(Car).get(id)

    def add(self, json):
        car = Car(model=json['model'], condition=json['condition'], price=json['price'])

        self.db.session.add(car)
        self.db.session.commit()

        return car

    def update(self, car):
        self.db.session.commit()

    def delete(self, car):
        self.db.session.delete(car)
        self.db.session.commit()

