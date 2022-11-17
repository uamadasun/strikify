#make sure to install your virtual environment as 'pipenv install flask pymysql flask-bcrypt'
from flask import Flask
app = Flask(__name__)
app.secret_key ='secret key'
