from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# SQLAlchemy
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)

# Flask
app = Flask(__name__)

@app.route("/")
@app.route("/restaurants/")
def restaurants():

    try:
        session = DBSession()
        restaurants = session.query(Restaurant).all()
        return render_template("restaurants.html", restaurants=restaurants)

    finally:
        if session:
            session.close()

# leave the trailing slash to allow Flask to execute this route regardless of whether the trailing slash is there or not
@app.route("/restaurant/<int:restaurant_id>/")
def restaurant_menu(restaurant_id):
    try:

        session = DBSession()
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        if restaurant is None:
            return render_template("404.html"), 404

        menu_items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
        return render_template("menu.html", restaurant=restaurant, items=menu_items)

    finally:

        if session:
            session.close()

@app.route("/restaurant/<int:restaurant_id>/JSON/")
def JSON_restaurant_menu(restaurant_id):
    try:

        session = DBSession()
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        if restaurant is None:
            return jsonify(MenuItems=[]), 404

        menu_items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
        return jsonify(MenuItems=[i.serialize for i in menu_items]), 200

    finally:

        if session:
            session.close()

@app.route("/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON/")
def JSON_restaurant_menu_item(restaurant_id, menu_id):
    try:

        session = DBSession()
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        menu_item = session.query(MenuItem).filter_by(id=menu_id, restaurant_id=restaurant_id).one()
        if restaurant is None or menu_item is None:
            return jsonify([]), 404

        return jsonify(menu_item.serialize)

    finally:

        if session:
            session.close()

# Task 1: Create route for newMenuItem function here
@app.route("/restaurant/<int:restaurant_id>/new/", methods=["GET", "POST"])
def new_menu_item(restaurant_id):

    try:

        session = DBSession()

        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        if restaurant is None:
            return render_template("404.html"), 404
        
        if request.method == "GET":
            return render_template("newmenuitem.html", restaurant_id=restaurant_id)

        if request.method == "POST":
            new_item = MenuItem(name=request.form["name"], course=request.form["course"], description=request.form["description"], price=request.form["price"], restaurant_id=restaurant_id)
            session.add(new_item)
            session.commit()

            flash("Menu item created successfully!")

        return redirect(url_for("restaurant_menu", restaurant_id=restaurant_id))

    finally:

        if session:
            session.close()

# Task 2: Create route for editMenuItem function here
@app.route("/restaurant/<int:restaurant_id>/<int:menu_id>/edit/", methods=["GET", "POST"])
def edit_menu_item(restaurant_id, menu_id):

    try:

        session = DBSession()

        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        menu_item = session.query(MenuItem).filter_by(id=menu_id, restaurant_id=restaurant_id).one()

        if restaurant is None or menu_item is None:
            return render_template("404.html"), 404
        
        if request.method == "GET":
            return render_template("editmenuitem.html", restaurant_id=restaurant_id, item=menu_item)

        if request.method == "POST":
            menu_item.name = request.form["name"]
            menu_item.course = request.form["course"]
            menu_item.description = request.form["description"]
            menu_item.price = request.form["price"]

            session.add(menu_item)
            session.commit()

            flash("Menu item edited successfully!")

        return redirect(url_for("restaurant_menu", restaurant_id=restaurant_id), code=303)

    finally:

        if session:
            session.close()

# Task 3: Create a route for deleteMenuItem function here
@app.route("/restaurant/<int:restaurant_id>/<int:menu_id>/delete/", methods=["GET", "POST"])
def delete_menu_item(restaurant_id, menu_id):
    
    try:

        session = DBSession()

        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        menu_item = session.query(MenuItem).filter_by(id=menu_id, restaurant_id=restaurant_id).one()

        if restaurant is None or menu_item is None:
            return render_template("404.html"), 404
        
        if request.method == "GET":
            return render_template("deletemenuitem.html", restaurant_id=restaurant_id, item=menu_item)

        if request.method == "POST":
            session.delete(menu_item)
            session.commit()

            flash("Menu item deleted successfully!")

        return redirect(url_for("restaurant_menu", restaurant_id=restaurant_id))

    finally:

        if session:
            session.close()

# the condition means the if gets triggered only if the script is called via the interpreter
if __name__ == "__main__":
    app.secret_key = "a_secret_key_for_production"
    app.debug = True
    app.run(host = "127.0.0.1", port = 5000)
