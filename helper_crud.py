from re import search
from market import app
from market.models  import User, Item, db
from random import randrange
from time import sleep
from winsound import Beep
from flask_bcrypt import Bcrypt
import os

bcrypt = Bcrypt(app)

def create_tables():
	db.create_all()

################################ USERS
def get_all_users():
    os.system("cls")
    users = User.query.all()
    for user in users:
        sleep(0.20)
        print(user)
        Beep(500,50)


def add_user(username, email_address, password_hash):
	password_hash = bcrypt.generate_password_hash(password_hash)
	new_user = User(username=username, email_address=email_address, password_hash=password_hash)
	db.session.add(new_user)
	db.session.commit()


def get_one_user(id):
	search_result = User.query.filter_by(id=id).first()
	if search_result != None:
		print(search_result)
	else:
		print("Record not found")

def set_update_user(id=id):
	user = User.query.filter_by(id=id).first()
	username = user.username
	email_address = user.email_address
	budget = user.budget
	print("Update user {}".format(user.username))
	sleep(.50)
	print("Current email: ", user.email_address)
	sleep(.50)
	email_address = input("Enter new email: ")
	sleep(0.50)
	print("Current budget: ", user.budget)
	sleep(0.50)
	budget = int(input("Update budget "))
	User.query.filter_by(id=id).update(dict(email_address=email_address, budget=budget))
	db.session.commit()

def delete_user(id):
	user = User.query.filter_by(id=id).first()
	db.session.delete(user)
	db.session.commit()
	print("Record has been deleted")

################################ ITEMS
"""
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(length=32), nullable=False, unique=True)
	price = db.Column(db.Integer(), nullable=False)
	barcode = db.Column(db.String(length=12), nullable=False, unique=True)
	description = db.Column(db.Text(), nullable=False)
	owner = db.Column(db.Integer(), db.ForeignKey("user.id"))
"""
def get_all_items():
    os.system("cls")
    items = Item.query.all()
    for item in items:
        sleep(0.02)

        print(item)

def add_new_item(name, price, description, owner):
	def get_barcode(barcode):
		barcode = randrange(111111111111,999999999999)
		print(barcode)
		sleep(2)
		item = Item.query.filter_by(barcode=barcode).first()
		print(item)
		sleep(2)
		if item == None:
			return str(barcode)
		else:
			get_barcode(barcode)

	barcode = ""
	barcode = get_barcode(barcode)
	print("Barcode out of the function: ", barcode)
	sleep(3)
	new_item = Item(name=name, price=price, barcode=barcode, description=description, owner=owner)
	db.session.add(new_item)
	db.session.commit()


def get_one_item(id):
	search_result = Item.query.filter_by(id=id).first()
	if search_result != None:
		print(search_result)
	else:
		print("Record not found")

def set_update_item(id):
	item = Item.query.filter_by(id=id).first()
	name = item.name
	price = item.price
	description = item.description
	print("Updating Item: ", item.name)
	name = input("Enter new name: ")
	sleep(0.50)
	print("Current price: ", item.price)
	sleep(0.50)
	price = int(input("Enter new price: "))
	sleep(0.50)
	print("Current description: ", item.description)
	description = input("Update description: ")
	Item.query.filter_by(id=id).update(dict(name=name, price=price, description=description))
	db.session.commit()
	print("Item has been updates!")
	sleep(0.50)
	get_one_item(id)


def delete_item(id):
	item = Item.query.filter_by(id=id).first()
	db.session.delete(item)
	db.session.commit()
	print("Record has been deleted!")
