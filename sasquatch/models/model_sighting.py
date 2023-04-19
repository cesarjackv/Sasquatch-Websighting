from sasquatch import app
from sasquatch.config.mysqlconnection import connectToMySQL
from sasquatch.models.model_user import User, flash, bcrypt


class Sighting:
    db = 'sasquatch'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.descr = data['descr']
        self.num = data['num']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']

    @staticmethod
    def valid_sighting(data):
        is_valid = True
        if len(data['name']) < 3:
            flash('Invalid name')
            is_valid = False
        if len(data['descr']) < 3:
            flash('Invalid descr')
            is_valid = False
        if int(data['num']) < 0:
            flash('Invalid number')
            is_valid = False
        if not data['date']:
            flash('Choose a date')
            is_valid = False
        return is_valid
    
    @classmethod
    def all_sightings(cls):
        query = "SELECT * FROM sightings LEFT JOIN users ON users.id = sightings.users_id;"
        results = connectToMySQL(cls.db).query_db(query)
        sightings = []
        for row in results:
            username = {
                **row,
                'id' : row['users.id'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            row = cls(row)
            row.user = User(username)
            sightings.append(row)
        return sightings

    @classmethod
    def new_sighting(cls, data):
        query = "INSERT INTO sightings (name, descr, num, date, users_id) VALUES (%(name)s, %(descr)s, %(num)s, %(date)s, %(users_id)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def edit_sighting(cls, data):
        query = "UPDATE sightings SET name = %(name)s, descr = %(descr)s, num = %(num)s, date = %(date)s, updated_at = now() WHERE id = %(user_id)s"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def one_sighting(cls, data):
        query = "SELECT * FROM sightings JOIN users ON users.id = sightings.users_id WHERE sightings.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            for row in results:
                username = {
                    **row,
                    'id' : row['users.id'],
                    'created_at' : row['users.created_at'],
                    'updated_at' : row['users.updated_at']
                }
            row = cls(row)
            row.user = User(username)
            return row

    @classmethod
    def delete_sighting(cls, data):
        query  = "DELETE FROM sightings WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)