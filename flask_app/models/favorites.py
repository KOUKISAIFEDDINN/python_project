from flask_app.configs.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models.user import User
from flask_app.models.property import Property

class Favorites:
    def __init__(self, data):
        self.id = data["favorites_id"]
        self.user_id = data["user_id"]
        self.property_id = data["property_id"]
        self.created_at = data["created_at"]

    # @classmethod
    # def create(cls, data):
    #     query = """
    #             INSERT INTO favorites (user_id, property_id, created_at)
    #             VALUES (%(user_id)s, %(property_id)s, %(created_at)s)
    #             """
    #     favorites_id = connectToMySQL(DATABASE).query_db(query, data)
    #     return favorites_id
    
    @classmethod
    def get_favorite_properties(cls, user_id):
        query = """
            SELECT * FROM properties WHERE property_id IN 
            (SELECT property_id FROM favorites WHERE user_id = %s)
        """
        data = (user_id,)
        results = connectToMySQL(DATABASE).query_db(query, data)
        favorite_properties = []
        if results:
            for row in results:
                favorite_properties.append(Property(row))  # Assuming Property class with appropriate constructor
        return favorite_properties

    
    @classmethod
    def is_favorite(cls, user_id, property_id):
        query = "SELECT COUNT(*) FROM favorites WHERE user_id = %s AND property_id = %s"
        data = (user_id, property_id)
        result = connectToMySQL(DATABASE).query_db(query, data)
        return bool(result[0]['COUNT(*)'])

    @classmethod
    def add_to_favorites(cls, data):
        query = "INSERT INTO favorites (user_id, property_id) VALUES (%s, %s)"
        favorite_id = connectToMySQL(DATABASE).query_db(query, (data['user_id'], data['property_id']))
        return favorite_id


    @classmethod
    def delete_favorite(cls, property_id):
        query = "DELETE FROM favorites WHERE property_id = %s"
        data = (property_id,)
        connectToMySQL(DATABASE).query_db(query, data)

    # #* =========== DELETE ===========
    # @classmethod
    # def delete_favorite(cls, id):
    #     query = "DELETE FROM favorites WHERE user_id = %s AND property_id = %s"
    #     connectToMySQL(DATABASE).query_db(query, {'id': id})