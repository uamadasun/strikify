from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import shop_model

from flask import flash
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.strike_username = data['strike_username']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod 
    def register_user(cls, data):
        query = """
        INSERT INTO users (strike_username, password)
        VALUES(%(strike_username)s, %(password)s);
        """
        return connectToMySQL('strikify_schema').query_db(query,data)

    @classmethod
    def get_by_username(cls, data):
        query = '''
        SELECT * FROM users
        WHERE users.strike_username = %(strike_username)s;
        '''
        
        user = connectToMySQL('strikify_schema').query_db(query, data)
        print(user)
        #if you get a tuple out of index error, it's because the email is not in the database and you're trying to return an index that isn't there so add this conditional.
        if len(user) > 0:
            return cls(user[0])
        return False

    @classmethod
    def get_by_id(cls, data):
        query = '''
        SELECT * FROM users
        WHERE users.id = %(id)s;
        '''
        return connectToMySQL('strikify_schema').query_db(query, data)




    @staticmethod
    def validate_user(data):
        is_valid = True

        if not len(data['password']) >= 8:
            flash('Password must be greater than 8 characters.')
            is_valid = False

        elif not data['password'] == data['confirm_password']:
            flash('Passwords must match.')
            is_valid = False

        #check if the username provided on registration is unique
        user_data = {
            'strike_username':data['strike_username']
        }
        potential_user = User.get_by_username(user_data)
        #print(potential_user)
        if potential_user:
            flash('Username already in the system. Use another username or log in.')
            is_valid = False

        return is_valid