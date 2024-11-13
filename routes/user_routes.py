from bson import ObjectId
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import mongo

user_bp = Blueprint('user', __name__)

# Obtener todos los usuarios
@user_bp.route('/users', methods=['GET'])
def get_users():
    try:
        users = mongo.users.find()  # Acceder a la colección de usuarios
        result = []
        for user in users:
            user['_id'] = str(user['_id'])  # Conversión de ObjectId a string
            result.append(user)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Manejo de excepciones

# Ruta para obtener el perfil del usuario autenticado
@user_bp.route('/user/profile', methods=['GET'])
@jwt_required()  # Esta ruta requiere autenticación JWT
def get_user_profile():
    try:
        # Obtener el ID del usuario del JWT
        user_id = get_jwt_identity()

        # Buscar al usuario en la base de datos usando el ID del JWT
        user = mongo.users.find_one({"_id": ObjectId(user_id)})

        if user is None:
            return jsonify({"error": "Usuario no encontrado"}), 404

        # Excluir la contraseña del usuario para no exponerla
        user_data = {
            "name": user["name"],
            "lastname": user["lastname"],
            "email": user["email"],
            "phone": user["phone"],
            "address": user["address"],
            "rol": user["rol"]
        }

        return jsonify(user_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Devuelve un error si ocurre una excepción
