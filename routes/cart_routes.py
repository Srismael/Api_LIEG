from flask import Blueprint, jsonify, request
from bson import ObjectId
from config import mongo

cart_bp = Blueprint('cart', __name__)

# Función auxiliar para convertir ObjectId a string
def convert_objectid_to_str(cart):
    cart['_id'] = str(cart['_id'])  # Convertir _id a string
    # Si hay otros campos con ObjectId, también conviértelos a string aquí si es necesario
    return cart


@cart_bp.route('/shopping_carts/<id_user>', methods=['GET'])
def get_cart_by_user(id_user):
    try:
        cart_items = mongo.shopping_cart.find({"id_user": id_user})
        result = [convert_objectid_to_str(item) for item in cart_items]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Ruta para añadir productos al carrito (actualizada)
@cart_bp.route('/shopping_carts', methods=['POST'])
def add_to_cart():
    try:
        data = request.get_json()
        id_user = data.get('id_user')
        id_product = data.get('id_product')
        price_cart = data.get('price_cart')

        if not id_user or not id_product or not price_cart:
            return jsonify({"error": "Missing fields"}), 400

        # Verificar disponibilidad del producto
        product = mongo.product.find_one({"_id": ObjectId(id_product)})
        if not product:
            return jsonify({"error": "Product not found"}), 404

        if product['stock'] < 1:
            return jsonify({"error": "Product is out of stock"}), 400

        cart_item = {
            "id_user": id_user,
            "id_product": id_product,
            "price_cart": price_cart
        }
        mongo.shopping_cart.insert_one(cart_item)
        return jsonify({"message": "Product added to cart"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
    # Eliminar un producto del carrito
@cart_bp.route('/shopping_carts/<cart_id>', methods=['DELETE'])
def remove_from_cart(cart_id):
    try:
        mongo.shopping_cart.delete_one({"_id": ObjectId(cart_id)})
        return jsonify({"message": "Product removed from cart"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
