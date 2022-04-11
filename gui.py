import requests
import tkinter as tk
from tkinter import *


# layout finished, need to implement the actual requests portion later.

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Alex's bad rentals", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Manage Customers",
                  command=lambda: master.switch_frame(customer_handler)).pack()
        tk.Button(self, text="Manage Cars",
                  command=lambda: master.switch_frame(car_handler)).pack()
        tk.Button(self, text="Edit a relation",
                  command=lambda: master.switch_frame(relation_handler)).pack()
        self.btn_quit = Button(self)
        self.btn_quit = Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.btn_quit.pack()


class customer_handler(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        tk.Frame.configure(self, bg='cyan')
        tk.Label(self, text="Manage Customers", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)

        tk.Button(self, text="Add", command=lambda: master.switch_frame(add_customer)).pack()

        tk.Button(self, text="Edit",
                  command=lambda: master.switch_frame(edit_customer)).pack()
        tk.Button(self, text="Remove",
                  command=lambda: master.switch_frame(remove_customer)).pack()
        tk.Button(self, text="Back",
                  command=lambda: master.switch_frame(StartPage)).pack()


class add_customer(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        L1 = Label(self, text='Enter name')
        L1.grid(row=0, column=0)
        self.entry_name = Entry(self)
        self.entry_name.grid(row=0, column=1)

        L2 = Label(self, text='Enter email')
        L2.grid(row=1, column=0)
        self.entry_email = Entry(self)
        self.entry_email.grid(row=1, column=1)

        L3 = Label(self, text='Enter date')
        L3.grid(row=2, column=0)
        self.entry_date = Entry(self)
        self.entry_date.grid(row=2, column=1)
        self.btn_model = Button(self, text='Add customer', command=self.add_handler)
        self.btn_model.grid(row=3, column=0)
        tk.Button(self, text="Back",
                  command=lambda: master.switch_frame(customer_handler)).grid(row=3, column=1)

    def add_handler(self):
        name = self.entry_name.get()
        email = self.entry_email.get()
        date = self.entry_date.get()
        customer = {
            "name": name,
            "email": email,
            "date": date
        }
        result = requests.post('http://localhost:5000/customers/', json=customer)
        customer = result.json()
        if result.status_code == 201:
            test = tk.Label(self, text=f'Customer added with id = {customer["id"]}',
                            font=('Helvetica', 18, "bold"))
            test.grid(row=4, column=1)
            self.after(5000, test.destroy)
        else:
            test = tk.Label(self, text=f'Failed with status code : {result.status_code}',
                            font=('Helvetica', 18, "bold"))
            test.grid(row=4, column=1)
            self.after(5000, test.destroy)
        self.entry_name.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.entry_date.delete(0, 'end')


class edit_customer(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        L1 = Label(self, text='Enter Customer id to edit')
        L1.grid(row=0, column=0)
        self.entry_id = Entry(self)
        self.entry_id.grid(row=0, column=1)
        self.btn_model = Button(self, text='Edit customer', command=self.edit_handler)
        self.btn_model.grid(row=1, column=0)
        tk.Button(self, text="Back",
                  command=lambda: master.switch_frame(customer_handler)).grid(row=1, column=1)

    def edit_handler(self):
        customer_id = self.entry_id.get()
        customer = requests.get(f'http://localhost:5000/customers/{customer_id}')
        if customer:
            L1 = Label(self, text='name')
            L1.grid(row=7, column=0)
            self.entry_name = Entry(self)
            self.entry_name.grid(row=7, column=1)

            L2 = Label(self, text='email')
            L2.grid(row=8, column=0)
            self.entry_email = Entry(self)
            self.entry_email.grid(row=8, column=1)

            L3 = Label(self, text='date')
            L3.grid(row=9, column=0)
            self.entry_date = Entry(self)
            self.entry_date.grid(row=9, column=1)

            self.btn_commit = Button(self)
            self.btn_commit = Button(self, text="commit", fg="blue", command=self.commit_add)
            self.btn_commit.grid(row=10, column=0)

        else:
            test = tk.Label(self, text=f'Customer not found with id {customer_id}',
                            font=('Helvetica', 18, "bold"))
            test.grid(row=10, column=1)
            self.after(2000, test.destroy)

    def commit_add(self):
        customer_id = self.entry_id.get()
        customer_name = self.entry_name.get()
        customer_email = self.entry_email.get()
        customer_date = self.entry_date.get()
        edited_customer = {
            "name": customer_name,
            "email": customer_email,
            "date": customer_date
        }
        response = requests.put(f'http://localhost:5000/customers/{customer_id}', json=edited_customer)
        if response.status_code == 200:
            test = tk.Label(self, text=f'Customer edited with id: {customer_id}',
                            font=('Helvetica', 18, "bold"))
            test.grid(row=10, column=1)
            self.after(5000, test.destroy)
        else:
            test = tk.Label(self, text=f'Failed with status code : {response.status_code}',
                            font=('Helvetica', 18, "bold"))
            test.grid(row=10, column=1)
            self.after(5000, test.destroy)


class remove_customer(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        L1 = Label(self, text='Enter customer to remove')
        L1.grid(row=0, column=0)
        self.entry_remove = Entry(self)
        self.entry_remove.grid(row=0, column=1)

        self.btn_model = Button(self, text='Remove customer', command=self.remove_commit)
        self.btn_model.grid(row=1, column=0)
        tk.Button(self, text="Back",
                  command=lambda: master.switch_frame(customer_handler)).grid(row=1, column=1)

    def remove_commit(self):
        customer_id = self.entry_remove.get()
        response = requests.delete(f'http://localhost:5000/customers/{customer_id}')
        if response.status_code == 200:
            test = tk.Label(self, text=f'Customer removed with id: {customer_id}',
                            font=('Helvetica', 18, "bold"))
            test.grid(row=2, column=0)
            self.after(5000, test.destroy)
        else:
            test = tk.Label(self, text=f'Failed with status code : {response.status_code}',
                            font=('Helvetica', 18, "bold"))
            test.grid(row=2, column=0)
            self.after(5000, test.destroy)


class car_handler(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg='red')
        tk.Label(self, text="Manage Cars", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Add",
                  command=lambda: master.switch_frame(add_car)).pack()
        tk.Button(self, text="Edit",
                  command=lambda: master.switch_frame(edit_car)).pack()
        tk.Button(self, text="Remove",
                  command=lambda: master.switch_frame(remove_car)).pack()
        tk.Button(self, text="Back",
                  command=lambda: master.switch_frame(StartPage)).pack()


class add_car(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        L1 = Label(self, text='Enter model')
        L1.grid(row=0, column=0)
        self.entry_model = Entry(self)
        self.entry_model.grid(row=0, column=1)

        L2 = Label(self, text='Enter condition')
        L2.grid(row=1, column=0)
        self.entry_condition = Entry(self)
        self.entry_condition.grid(row=1, column=1)

        L3 = Label(self, text='Enter price')
        L3.grid(row=2, column=0)
        self.entry_price = Entry(self)
        self.entry_price.grid(row=2, column=1)

        # L4 = Label(self, text='Enter customer id')
        # L4.grid(row=3, column=0)
        # self.entry_customer_id = Entry(self)
        # self.entry_customer_id.grid(row=3, column=1)

        self.btn_model = Button(self, text='Add car', command=self.add_car_handler)
        self.btn_model.grid(row=4, column=0)
        tk.Button(self, text="Back",
                  command=lambda: master.switch_frame(car_handler)).grid(row=4, column=1)

    def add_car_handler(self):
        model = self.entry_model.get()
        condition = self.entry_condition.get()
        price = self.entry_price.get()
        # customer_id = self.entry_customer_id
        car = {
            "model": model,
            "condition": condition,
            "price": price
        }
        result = requests.post('http://localhost:5000/cars/', json=car)
        response = result.json()
        if result.status_code == 201:
            test = tk.Label(self, text=f'Car added with id = {response["id"]}',
                            font=('Helvetica', 18, "bold"))
            test.grid(row=4, column=1)
            self.after(5000, test.destroy)
        else:
            test = tk.Label(self, text=f'Failed with status code : {result.status_code}',
                            font=('Helvetica', 18, "bold"))
            test.grid(row=4, column=1)
            self.after(5000, test.destroy)


class edit_car(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        L1 = Label(self, text='Enter Car id to edit')
        L1.grid(row=0, column=0)
        self.entry_id = Entry(self)
        self.entry_id.grid(row=0, column=1)
        self.btn_model = Button(self, text='Edit car', command=self.edit_car_handler)
        self.btn_model.grid(row=1, column=0)
        tk.Button(self, text="Back",
                  command=lambda: master.switch_frame(car_handler)).grid(row=1, column=1)

    def edit_car_handler(self):
        car_id = self.entry_id.get()
        car = requests.get(f'http://localhost:5000/cars/{car_id}')
        if car:
            newL2 = Label(self, text='New model')
            newL2.grid(row=7, column=0)
            self.entry_model = Entry(self)
            self.entry_model.grid(row=7, column=1)

            newL2 = Label(self, text='New condition')
            newL2.grid(row=8, column=0)
            self.entry_condition = Entry(self)
            self.entry_condition.grid(row=8, column=1)

            newL3 = Label(self, text='New price')
            newL3.grid(row=9, column=0)
            self.entry_price = Entry(self)
            self.entry_price.grid(row=9, column=1)

            self.btn_commit = Button(self)
            self.btn_commit = Button(self, text="commit", fg="blue", command=self.commit_add_car)
            self.btn_commit.grid(row=10, column=0)
        else:
            test = tk.Label(self, text=f'Car not found',
                            font=('Helvetica', 18, "bold"))
            test.grid(row=10, column=1)
            self.after(2000, test.destroy)

    def commit_add_car(self):
        car_id = self.entry_id.get()
        model = self.entry_model.get()
        condition = self.entry_condition.get()
        price = self.entry_price.get()
        car = {
            "model": model,
            "condition": condition,
            "price": price
        }
        response = requests.put(f'http://localhost:5000/cars/{car_id}', json=car)
        print(f'{response.status_code}')
        if response.status_code == 200:
            test = tk.Label(self, text=f'Car edited with id: {car_id}',
                            font=('Helvetica', 18, "bold"))
            test.grid(row=10, column=1)
            self.after(5000, test.destroy)
        else:
            test = tk.Label(self, text=f'Failed with status code : {response.status_code}',
                            font=('Helvetica', 18, "bold"))
            test.grid(row=10, column=1)
            self.after(5000, test.destroy)


class remove_car(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        L1 = Label(self, text='Enter car to remove')
        L1.grid(row=0, column=0)
        self.entry_remove = Entry(self)
        self.entry_remove.grid(row=0, column=1)
        self.btn_model = Button(self, text='Remove car', command=self.remove_commit)
        self.btn_model.grid(row=1, column=0)
        tk.Button(self, text="Back",
                  command=lambda: master.switch_frame(car_handler)).grid(row=1, column=1)

    def remove_commit(self):
        car_id = self.entry_remove.get()
        response = requests.delete(f'http://localhost:5000/cars/{car_id}')
        if response.status_code == 200:
            test = tk.Label(self, text=f'Car removed with id: {car_id}',
                            font=('Helvetica', 18, "bold"))
            test.grid(row=2, column=1)
            self.after(5000, test.destroy)
        else:
            test = tk.Label(self, text=f'Failed with status code : {response.status_code}',
                            font=('Helvetica', 18, "bold"))
            test.grid(row=2, column=1)
            self.after(5000, test.destroy)


class relation_handler(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg='orange')
        tk.Label(self, text="Assign a relation", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Assign relation",
                  command=self.assign_relation).pack(side="bottom")
        tk.Button(self, text="Remove relation",
                  command=self.remove_relation).pack(side="bottom")
        L1 = Label(self, text='Enter customer')
        L1.pack(side="left")
        self.entry_customer = Entry(self)
        self.entry_customer.pack(side="left")
        L2 = Label(self, text='Enter car')
        L2.pack(side="left")
        self.entry_car = Entry(self)
        self.entry_car.pack(side="left")
        tk.Button(self, text="Back",
                  command=lambda: master.switch_frame(StartPage)).pack()

    def assign_relation(self):
        customer_id = self.entry_customer.get()
        car_id = self.entry_car.get()
        customer = requests.get(f'http://localhost:5000/customers/{customer_id}')
        car = requests.get(f'http://localhost:5000/cars/{car_id}')
        response_customer = customer.json()
        response_car = car.json()
        print(response_car)
        new_relation = {
            'model': response_car["model"],
            'condition': response_car["condition"],
            'price': response_car["price"],
            'customer_id': response_customer["id"]
        }
        print(new_relation)
        result = requests.put(f'http://localhost:5000/cars/{response_car["id"]}', data=new_relation)
        if result.status_code == 201:
            test = tk.Label(self, text=f'Relation created with car id {response_car["id"]} and {response_customer["id"]}',
                     font=('Helvetica', 18, "bold"))
            test.pack(side="bottom")
            self.after(5000, test.destroy)
        else:
            test = tk.Label(self, text=f'Failed with status code : {result.status_code}',
                     font=('Helvetica', 18, "bold"))
            test.pack(side="bottom")
            self.after(5000, test.destroy)

    def remove_relation(self):
        pass


def main():
    app = Application()

    app.mainloop()


if __name__ == '__main__':
    main()
