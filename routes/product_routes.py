from flask import Blueprint, jsonify, request
from bson import ObjectId
from config import mongo
from utils.validation import validate_product

product_bp = Blueprint('product', __name__)

# Obtener todos los productos
@product_bp.route('/products', methods=['GET'])
def get_products():
    products = mongo.product.find()
    result = []
    for product in products:
        # Convertir ObjectId a string y agregar el producto a la lista
        product['_id'] = str(product['_id'])  # Conversión a string
        result.append(product)
    return jsonify(result)
