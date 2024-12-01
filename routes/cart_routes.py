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
        print("Received data:", data)  # Para ver los datos que está recibiendo

        id_user = data.get('id_user')
        if not id_user:
            return jsonify({"error": "Missing 'id_user' field"}), 400

        products = data.get('products')
        if not products:
            return jsonify({"error": "Missing 'products' field"}), 400
        
        # Verificar cada producto
        for product in products:
            product_id = product.get('id_product')
            if not product_id:
                return jsonify({"error": "Missing 'id_product' in product"}), 400

            # Verificar si el producto existe
            product_db = mongo.product.find_one({"_id": ObjectId(product_id)})
            if not product_db:
                return jsonify({"error": f"Product {product_id} not found"}), 404

        total_cart = data.get('total_cart')
        if total_cart is None:
            return jsonify({"error": "Missing 'total_cart' field"}), 400

        # Si todo es correcto, agregar el carrito a la base de datos
        cart_item = {
            "id_user": id_user,
            "products": products,
            "total_cart": total_cart
        }
        mongo.shopping_cart.insert_one(cart_item)
        return jsonify({"message": "Product added to cart"}), 201

    except Exception as e:
        print("Error occurred:", str(e))  # Imprimir el error en la consola para depuración
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


    
    # Eliminar un producto del carrito
@cart_bp.route('/shopping_carts/<cart_id>', methods=['DELETE'])
def remove_from_cart(cart_id):
    try:
        mongo.shopping_cart.delete_one({"_id": ObjectId(cart_id)})
        return jsonify({"message": "Product removed from cart"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
