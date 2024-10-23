from flask import Blueprint, jsonify, request
from bson import ObjectId
from config import mongo

cart_bp = Blueprint('cart', __name__)

# Función auxiliar para convertir ObjectId a string
def convert_objectid_to_str(cart):
    cart['_id'] = str(cart['_id'])  # Convertir _id a string
    # Si hay otros campos con ObjectId, también conviértelos a string aquí si es necesario
    return cart

# Obtener todos los carritos
@cart_bp.route('/shopping_carts', methods=['GET'])
def get_shopping_carts():
    carts = mongo.shopping_cart.find()
    result = [convert_objectid_to_str(cart) for cart in carts]
    return jsonify(result)
