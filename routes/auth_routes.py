# auth_routes.py
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from config import mongo

auth_bp = Blueprint('auth', __name__)

# Ruta de registro
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    lastname = data.get('lastname')
    email = data.get('email')
    password = data.get('password')
    phone = data.get('phone')
    rol = data.get('rol', 'usuario')  # Asignar rol por defecto "usuario"
    address = data.get('address')

    # Verificar si el correo electrónico ya existe
    if mongo.users.find_one({"email": email}):
        return jsonify({"error": "Email already exists"}), 409

    # Crear el hash de la contraseña y almacenar el nuevo usuario
    hashed_password = generate_password_hash(password)
    mongo.users.insert_one({
        "name": name,
        "lastname": lastname,
        "email": email,
        "password": hashed_password,
        "phone": phone,
        "rol": rol,
        "address": address
    })
    return jsonify({"message": "User registered successfully"}), 201

# Ruta de inicio de sesión
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Buscar el usuario por correo electrónico
    user = mongo.users.find_one({"email": email})
    if user and check_password_hash(user["password"], password):
        # Crear el token JWT con el ID del usuario y su rol
        access_token = create_access_token(identity=str(user['_id']), additional_claims={"rol": user["rol"]})
        return jsonify(access_token=access_token), 200

    return jsonify({"error": "Invalid credentials"}), 401

# Ruta protegida de ejemplo
@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    return jsonify(logged_in_as=user_id), 200
