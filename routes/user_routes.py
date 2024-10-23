from flask import Blueprint, jsonify, request
from bson import ObjectId
from config import mongo

user_bp = Blueprint('user', __name__)

# Obtener todos los usuarios
@user_bp.route('/users', methods=['GET'])
def get_users():
    try:
        users = mongo.users.find()  # Use mongo to access the collection
        result = []
        for user in users:
            user['_id'] = str(user['_id'])  # Conversión a string
            result.append(user)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Devuelve un error si ocurre una excepción
