from market import app
from flask import render_template, url_for, redirect, flash, get_flashed_messages, request, jsonify
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user

###########################
#-- API use direct MySQL
import mysql.connector
from mysql.connector import Error
from random import randrange
##########################


@app.route("/")
# @app.route("/home")
def home():
	return redirect(url_for("market"))


@app.route("/market", methods=["GET", "POST"])
@login_required
def market():
	purchase_form = PurchaseItemForm()
	sell_form = SellItemForm()

	if request.method == "POST":
		purchased_item = request.form.get("purchased_item")

		p_item_object = Item.query.filter_by(id=purchased_item).first()

		if p_item_object:
			p_item_object.price = p_item_object.price / 10 #--budget need to be fixed
			if current_user.budget >= p_item_object.price:
				p_item_object.owner = current_user.id

				current_user.budget -= p_item_object.price
				db.session.commit()
				flash("Purchase successful!", category="success")

			else:
				flash("Not sufficient funds", category="danger")

		sold_item = request.form.get("sold_item")
		item_for_sale = Item.query.filter_by(id=sold_item).first()
		if item_for_sale:
			item_for_sale.owner = None
			current_user.budget += item_for_sale.price
			db.session.commit()
			flash("Sell successful. Item back to market", category="success")

		print(sold_item)


	items = Item.query.filter_by(owner=None)

	owned_items = Item.query.filter_by(owner=current_user.id).all()

	return render_template("market.html", items=items, owned_items=owned_items, purchase_form=purchase_form, sell_form=sell_form)


@app.route("/about")
def about():
	return render_template("about.html")


@app.route("/register", methods=["GET", "POST"])
def register():
	form = RegisterForm()

	if form.validate_on_submit():
		new_user = User(username=form.username.data,
					    email_address=form.email_address.data,
					    password=form.password_1.data)
		db.session.add(new_user)
		db.session.commit()

		login_user(new_user)
		flash("Account created! you are logged in", category="success")

		return redirect(url_for("market"))

	if form.errors != {}:
		for err_msg in form.errors.values():
			flash(err_msg, category="danger")
			print(err_msg)
			print(type(err_msg))
	return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		current_user = User.query.filter_by(username=form.username.data).first()
		if current_user and current_user.check_password_correction(
			attempted_password=form.password.data
			):
				current_user = User.query.filter_by(username=form.username.data).first()
				login_user(current_user)
				flash("You are logged in", category="success")
				print(current_user.is_authenticated)

				return redirect(url_for("market"))
		else:
			flash("Username or password Not match", category="danger")


	return render_template("login.html", form=form)


@app.route("/logout")
def logout():
	logout_user()
	flash("You logged out!", category="info")
	return redirect(url_for("home"))

#############################################################
#-- API routes 

connection = mysql.connector.connect(host="localhost",
                                     database="market",
                                     user="root",
                                     password="root?9898")

@app.route("/api/ver0.1/items")
def api_get_items():
    cur = connection.cursor(dictionary=True)
    cur.execute("""SELECT * FROM item """)
    results = cur.fetchall()
    cur.close()

    return jsonify(results)

@app.route("/api/ver0.1/items/<string:name>", methods=["GET","POST", "PUT"])
def api_get_item(name):
    if request.method == "POST":
        input_body = request.get_json()
        name = input_body["name"]
        price = input_body["price"]
        barcode = randrange(000000000000,999999999999)
        description = input_body["description"]

        cur = connection.cursor(dictionary=True)
        sql = """INSERT INTO item (name, price, barcode, description) VALUES (%s,%s,%s,%s) """
        val = (name, price, barcode, description)
        cur.execute(sql,val)
        connection.commit()
        cur.close()
        return {"msg": "Item inserted"}


    elif request.method == "PUT":
        try:
            input_body = request.get_json()
            id = input_body["id"]
            name = input_body["name"]
            price = input_body["price"]
            barcode = input_body["barcode"]
            description = input_body["description"]

            cur = connection.cursor(dictionary=True)

            query = """UPDATE item SET name=%s, price=%s, barcode=%s, description=%s WHERE id=%s """
            val = (name,price,barcode,description, id)
            cur.execute(query, val)
            connection.commit()
            cur.close()
            return {"msg": "Item Updated"}
        except Error:
            return{"msg": Error}


    elif request.method == "GET":
        cur = connection.cursor(dictionary=True)
        cur.execute("""SELECT * FROM item WHERE name='%s'"""%(name))
        result = cur.fetchone()
        cur.close()
        if result == None:
            return jsonify({"msg": "Not found"}, 404)
        else:
            return jsonify(result), 200


@app.route("/api/ver0.1/items/<string:name>", methods=["DELETE"])
def api_delete_item(name):
    cur = connection.cursor(dictionary=True)
    cur.execute("""DELETE FROM item WHERE name='%s'"""%(name))
    connection.commit()
    cur.close()

    return jsonify({name: "DELETED"}, 200)
