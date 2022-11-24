from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model
from flask_app import app
from flask import flash
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Shop:
    def __init__(self, data):
        self.id = data['id']
        self.shop_name = data['shop_name']
        self.owner_id = data['owner_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod 
    def create_shop(cls, data):
        query = """
        INSERT INTO shops (shop_name, owner_id)
        VALUES(%(shop_name)s, %(owner_id)s);
        """
        return connectToMySQL('strikify_schema').query_db(query,data)

    @classmethod
    def get_shop_of_user(cls,data):
        query = '''
        SELECT * FROM shops
        WHERE shops.owner_id = %(owner_id)s;
        '''
        
        shop = connectToMySQL('strikify_schema').query_db(query, data)
        if shop:
            return shop[0] #CHANGED FROM CLASS
        return False

    @classmethod 
    def add_product(cls, data):
        query = """
        INSERT INTO products (product_name, product_price, shop_id)
        VALUES(%(product_name)s, %(product_price)s, %(shop_id)s);
        """
        return connectToMySQL('strikify_schema').query_db(query,data)

    @classmethod
    def view_all_products(cls):
        query = """
        SELECT * FROM products
        ORDER BY product_name;
        """
        all_products = []
        results = connectToMySQL('strikify_schema').query_db(query)
        if not results:
            return False
        for row in results:
            all_products.append(row)
        return all_products


    @classmethod
    def view_all_products_by_user_id(cls, data):
        query = """
        SELECT * FROM products
        JOIN shops
        ON products.shop_id = shops.id
        WHERE shops.owner_id = %(owner_id)s
        ORDER BY product_name;
        """
        all_products = []
        results = connectToMySQL('strikify_schema').query_db(query, data)
        if not results:
            return False
        for row in results:
            all_products.append(row)
        return all_products

    @classmethod
    def delete_product(cls, data):
        query = """
        DELETE FROM products
        WHERE id = %(id)s;
        """
        return connectToMySQL('strikify_schema').query_db(query, data)

    @classmethod
    def create_shopping_cart(cls, data):
        query = """
        INSERT INTO shopping_cart (user_id)
        VALUES(%(user_id)s);
        """
        return connectToMySQL('strikify_schema').query_db(query,data)

    @classmethod
    def create_shopping_cart_item(cls, data):
        query = """
        INSERT INTO shopping_cart_item (shopping_cart_id, product_id)
        VALUES(%(shopping_cart_id)s, %(product_id)s);
        """
        return connectToMySQL('strikify_schema').query_db(query,data)


    @classmethod
    def get_items_by_cart_id(cls, data):
        query = '''
        SELECT * FROM shopping_cart_item
        JOIN products
        ON products.id = shopping_cart_item.product_id
        WHERE shopping_cart_id = %(shopping_cart_id)s;
        '''
        results = connectToMySQL('strikify_schema').query_db(query, data)
        if not results:
            return False
        all_items = []
        for row in results:
            all_items.append(row)
        return all_items
    
    @classmethod
    def get_product_by_id(cls, data):
        query = """
        SELECT * FROM products
        WHERE id = %(id)s;
        """
        return connectToMySQL('strikify_schema').query_db(query)

    @classmethod
    def delete_from_cart_items(cls,data):
        query = """
        DELETE FROM shopping_cart_item
        WHERE id = %(id)s;
        """
        return connectToMySQL('strikify_schema').query_db(query, data)

    @staticmethod
    def validate_product(data):
        is_valid = True

        if len(data['product_name']) < 1:
            flash('Product name is required.')
            is_valid = False

        if not data['product_price']:
            flash('Product price is required.')
            is_valid = False
        
        if not float(data['product_price']) > 0:
            flash('Product must be greater than $0.')
            is_valid = False
        

        return is_valid