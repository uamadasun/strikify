from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_app.models.shop_model import Shop
from flask_app.controllers import shop_controller
from flask_app.controllers import user_controller 
from flask_bcrypt import Bcrypt
from flask_app.key import token, webhook_key
import requests
import json
import random
from flask_qrcode import QRcode
import time

qrcode = QRcode(app)
bcrypt = Bcrypt(app)

@app.route('/')
def home_page():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('login_page.html')

#--------------------------------------------------
# #REGISTRATION PAGE
@app.route('/go_to_register_page')
def go_register():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('/registration_page.html')

@app.route('/register_user', methods = ['POST'])
def register_user():

    # 1. validate the form
    if not User.validate_user(request.form):
        return redirect('/go_to_register_page')

    #2. validate strike username
    url = f"https://api.strike.me/v1/accounts/handle/{request.form['strike_username']}/profile"
    payload={}
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    if not response:
        flash('User not found, try again.')
        return redirect('/go_to_register_page')

    results = response.json() 

    #3. create the hashed password
    hashed_password = bcrypt.generate_password_hash(request.form['password'])

    #3 create the data dictionary with the hashed password as the password
    data = {
        'strike_username' : request.form['strike_username'],
        'password' : hashed_password
    }

    #create the new user using the register_user method and set it to session['user_id']
    session['user_id'] = User.register_user(data)
    
    # print(session['current_id'])
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "owner_id": session['user_id']
    }
    shop = Shop.get_shop_of_user(data)
    all_products = Shop.view_all_products_by_user_id(data)


    return render_template("shop_dashboard.html", shop = shop, all_products=all_products)
#--------------------------------------------------
#LOGIN & LOGOUT ROUTES
@app.route('/login_user', methods = ['POST'])
def log_in():
    if 'user_id' in session:
        return redirect('/dashboard')
    data = {
        'strike_username' : request.form['username']
    }

    user_in_database = User.get_by_username(data)

    if not user_in_database:
        flash("Invalid login information. Try again!")
        return redirect('/')

    if not bcrypt.check_password_hash(user_in_database.password, request.form['password']):
        flash("Invalid login information. Try again!")
        return redirect('/')

    session['user_id'] = user_in_database.id #VERY IMPORTANT
    session['shopping_cart'] = Shop.create_shopping_cart({'user_id':session['user_id']})

    return redirect('/dashboard')

@app.route('/logout')
def log_out():
    if'user_id' in session:
        del session['user_id']
    if 'shopping_cart' in session:
        del session['shopping_cart']
    if 'shop_id' in session:
        del session['shop_id']

    return redirect('/')
#--------------------------------------------------
@app.route('/generate_invoice/<int:user_id>')
def generate_invoice(user_id):
    #1 GET USER'S STRIKE HANDLE
    this_user = User.get_by_id({'id':session['user_id']})
    handle = this_user.strike_username

    print("%%%%%%%%%%%%%%HANDLE", handle)


    #2 ISSUE A NEW INVOICE
        #Correlation ID should be the cart ID
        #Get all cart items to get subtotal
    all_cart_items = Shop.get_items_by_cart_id({'shopping_cart_id':session['shopping_cart']})
    print(all_cart_items)

    subtotal = 0
    if all_cart_items:
        for each_item in all_cart_items:
            subtotal += each_item['product_price']

    url = f"https://api.strike.me/v1/invoices/handle/{handle}"

    payload = json.dumps({
    "correlationId": session['shopping_cart'] + random.randint(0,1000),
    "description": "Invoice for Order " + str(session['shopping_cart']),
    "amount": {
        "currency": "USD",
        "amount": str(subtotal)
    }
    })

    print("PAYLOAD\n", payload)

    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer '+ token
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    issue_invoice_results = response.json()
    print("RESULTS OF ISSUING AN INVOICE: ", issue_invoice_results)

    #3 ISSUE NEW QUOTE FOR INVOICE****************
    url = f"https://api.strike.me/v1/invoices/{issue_invoice_results['invoiceId']}/quote"
    payload={}
    headers = {
    'Accept': 'application/json',
    'Content-Length': '0',
    'Authorization': 'Bearer ' + token
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    quote_results = response.json()

    print("***********RESULTS OF ISSUING NEW INVOICE QUOTE: \n", quote_results)

    #SUBSCRIBE TO WEBHOOK

    url = "https://api.strike.me/v1/subscriptions"


    payload = json.dumps({
    "webhookUrl": "https://kramerica_industries.com/webhook",
    "webhookVersion": "v1",
    "secret": webhook_key,
    "enabled": True,
    "eventTypes": [
        "invoice.created",
        "invoice.updated"
    ]
    })
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer ' + token
    }


    response = requests.request("POST", url, headers=headers, data=payload)
    webhook_results = response.json()

    print("```````` RESULTS OF webhook_results\n", webhook_results)
    #USE LNINVOICE TO MAKE QRCODE
    expired = False

    ln_invoice = quote_results['lnInvoice']

    return render_template('invoice.html', ln_invoice = ln_invoice, issue_invoice_results = issue_invoice_results)


@app.route('/payment_success')
def payment_success():
    return render_template ('payment_success.html')