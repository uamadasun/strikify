from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_app.models.shop_model import Shop
from flask_app.controllers import user_controller #[Model class name or file name if it's a one to many relationship]
from flask_app.key import token
import requests
import json
import qrcode
from PIL import Image

@app.route('/create_shop', methods = ['POST'])
def create_shop():
    data = {
        'shop_name':request.form['shop_name'],
        'owner_id':session['user_id']
    }

    Shop.create_shop(data)
    return redirect('/dashboard')

@app.route('/add_product')
def add_product():
    return render_template('add_product.html')

@app.route('/new_product', methods = ['POST'])
def new_product():
    if not Shop.validate_product(request.form):
        return redirect('/add_product')
    data = {
        'product_name':request.form['product_name'],
        'product_price':request.form['product_price'],
        'quantity_in_stock':request.form['quantity_in_stock'],
    }
    Shop.add_product(data)
    return redirect('/dashboard')

@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):
    data = {
        'id' : product_id
    }

    Shop.delete_product(data)
    return redirect ('/dashboard')

@app.route('/view_cart')
def view_cart():
    all_products = Shop.view_all_products()

    data = {
    'user_id': session['user_id']
    }

    if 'shopping_cart' not in session:
        session['shopping_cart'] = Shop.create_shopping_cart(data)

    print("Shopping Cart ID", session['shopping_cart'])

    all_cart_items = Shop.get_items_by_cart_id({'shopping_cart_id': session['shopping_cart']})
    checkout_quantity = 0
    if all_cart_items:
        for each_item in all_cart_items:
            checkout_quantity += 1

    return render_template('cart.html', all_products = all_products, all_cart_items = all_cart_items, checkout_quantity=checkout_quantity)

@app.route('/add_item_to_cart/<int:product_id>')
def add_cart_item(product_id):
    data = {
        'shopping_cart_id': session['shopping_cart'],
        'product_id': product_id
    }
    Shop.create_shopping_cart_item(data)

        
    return redirect('/view_cart')

@app.route('/checkout')
def checkout_link():
    all_cart_items = Shop.get_items_by_cart_id({'shopping_cart_id':session['shopping_cart']})
    print(all_cart_items)

    subtotal = 0
    if all_cart_items:
        for each_item in all_cart_items:
            subtotal += each_item['product_price']
    print(subtotal)

    return render_template ('checkout_page.html', all_cart_items = all_cart_items, subtotal = subtotal)

@app.route('/delete_from_cart/<int:item_id>')
def delete_from_cart(item_id):
    data = {
        'id':item_id
    }
    Shop.delete_from_cart_items(data)
    return redirect('/checkout')