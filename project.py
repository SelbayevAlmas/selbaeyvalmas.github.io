from flask import Flask, render_template, url_for,request,redirect,flash,jsonify

from db_setup import Base,Restaurant,MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/')
@app.route('https://selbaeyvalmas.github.io/restaurant/<int:restaurant_id>/menu/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def restaurantMenu(restaurant_id):
    restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
    # print(restaurant.name)
    items= session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    # for i in items:
    #     print(i.name,i.id)

    return render_template('menu.html',restaurant=restaurant,items=items)

# Task 1: Create route for newMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/new/',methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method=='POST':
        newItem = MenuItem(name=request.form['name'],restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash('New menu item created!')
        return  redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html',restaurant_id=restaurant_id)
# Task 2: Create route for editMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/',methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    menuName = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method=='POST':
        menuName.name = request.form['name']
        session.add(menuName)
        session.commit()
        flash('Menu item edited!')
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        return render_template('editMenuItem.html',restaurant_id=restaurant_id,menu_id=menu_id,menuName=menuName)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    menuName = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(menuName)
        session.commit()
        flash('Menu item deleted!')
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        return render_template("deleteMenuItem.html",restaurant_id=restaurant_id,menu_id=menu_id,menuName=menuName)

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    # restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems = [i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id,menu_id):
    items = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem = items.serialize)

if __name__=='__main__':
    app.secret_key = 'super_secret_key'
    app.degub = True
    app.run(host='0.0.0.0',port=5000)
