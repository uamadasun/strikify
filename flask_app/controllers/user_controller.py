from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_app.models.shop_model import Shop
from flask_app.controllers import shop_controller
from flask_app.controllers import user_controller 
from flask_bcrypt import Bcrypt
from flask_app.key import token
import requests
import json
import qrcode
from PIL import Image

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
    all_products = Shop.view_all_products()


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

    return redirect('/')
#--------------------------------------------------

# @app.route('/generate_invoice/<int: user_id>', methods = ['POST'])
# def pay_user(user_id):

#     this_merchant = User.get_by_id(user_id)
    
#     url = f"https://api.strike.me/v1/accounts/handle/{this_merchant['strike_username']}/profile"
#     payload={}
#     headers = {
#         'Accept': 'application/json',
#         'Authorization': 'Bearer ' + token
#     }
#     response = requests.request("GET", url, headers=headers, data=payload)
#     if not response:
#         flash('User not found, try again.')
#         return redirect('/go_to_register_page')

#     results = response.json()
#     print(results)

#     return redirect('/checkout')


    

















#     url = f"https://api.strike.me/v1/invoices/handle/{handle}"

#     payload = json.dumps({
#         "correlationId": request.form['correlationId'],
#         "description": request.form['description'],
#         "amount": {
#         "currency": "USD",
#         "amount": request.form['amount']
#         }
#     })
    
#     headers = {
#         'Content-Type': 'application/json',
#         'Accept': 'application/json',
#         'Authorization': 'Bearer ' + token
#     }

#     response = requests.request("POST", url, headers=headers, data=payload)
#     results = response.json()
#     # print (results)
#     return redirect(f"/create_invoice/{results['invoiceId']}")

# @app.route('/create_invoice/<invoiceId>')
# def invoice(invoiceId):
#     url = f"https://api.strike.me/v1/invoices/{invoiceId}/quote"

#     payload={}
#     headers = {
#     'Accept': 'application/json',
#     'Content-Length': '0',
#     'Authorization': 'Bearer ' + token
# }

#     response = requests.request("POST", url, headers=headers, data=payload)
#     results = response.json()
#     print(results)

#     img = qrcode.make(results['lnInvoice'])
#     img.save(f'invoice{invoiceId}.jpg')
    
#     return render_template('invoice.html', invoiceId = invoiceId)