from sasquatch import app
from sasquatch.config.mysqlconnection import connectToMySQL
from flask import flash
import re  
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class User:
    db = 'sasquatch'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    def valid_register(data):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query, data)
        if len(data['first_name']) < 3 or type(data['first_name']) != str:
            flash("Incorrect input for First Name.")
            is_valid=False
        if len(data['last_name']) < 3 or type(data['last_name']) != str:
            flash("Incorrect input for Last Name.")
            is_valid=False
        if len(results) >= 1:
            flash("Email already taken.")
            is_valid=False
        if len(data['password']) < 8:
            flash("Password too short.")
            is_valid=False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email!!!")
            is_valid=False
        if data['password'] != data['confirm']:
            flash("Passwords don't match")
            is_valid=False
        return is_valid

    @classmethod
    def create(cls, data):
        query = "INSERT into users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def login(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        info = cls(results[0])
        return info
    
    @classmethod
    def user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls( results[0])
