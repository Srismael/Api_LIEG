from flask import Blueprint, jsonify, request
from bson import ObjectId
from config import mongo
from datetime import datetime

sales_bp = Blueprint('sales', __name__)

# Función auxiliar para convertir ObjectId a string
def convert_objectid_to_str(sale):
    sale['_id'] = str(sale['_id'])  # Convertir _id a string
    return sale

# Obtener todas las ventas
@sales_bp.route('/sales', methods=['GET'])
def get_sales():
    sales = mongo.sales_control.find()
    result = [convert_objectid_to_str(sale) for sale in sales]
    return jsonify(result)

# Realizar una compra
@sales_bp.route('/sales/checkout', methods=['POST'])
def checkout():
    try:
        data = request.get_json()
        id_user = data.get('id_user')
        payment = data.get('payment')  # Método de pago
        address = data.get('address')  # Dirección de envío

        # Validar datos requeridos
        if not id_user or not payment or not address:
            return jsonify({"error": "Missing fields"}), 400

        # Obtener los productos del carrito del usuario
        cart_items = list(mongo.shopping_cart.find({"id_user": id_user}))
        if not cart_items:
            return jsonify({"error": "Cart is empty"}), 400

        # Verificar disponibilidad de inventario y calcular total
        total_sale = 0
        products_sales = []
        for item in cart_items:
            product = mongo.product.find_one({"_id": ObjectId(item['id_product'])})
            if not product:
                return jsonify({"error": f"Product {item['id_product']} not found"}), 404

            if product['stock'] < 1:
                return jsonify({"error": f"Product {product['name']} is out of stock"}), 400

            # Actualizar stock del producto
            mongo.product.update_one(
                {"_id": ObjectId(item['id_product'])},
                {"$inc": {"stock": -1}}
            )

            # Agregar producto a la lista de ventas
            products_sales.append({
                "id_product": item['id_product'],
                "quantity": 1,  # Asumimos cantidad fija en este caso
                "price_per_unit": product['price']
            })

            total_sale += product['price']

        # Crear registro de venta
        sale = {
            "id_sale": f"SALE{ObjectId()}",  # Generar ID único para la venta
            "id_user": id_user,
            "products_sales": products_sales,
            "total_sale": total_sale,
            "payment": payment,
            "shipping_status": "Pendiente",  # Estado inicial del envío
            "address": address,
            "date_sale": datetime.utcnow().isoformat()  # Fecha actual
        }
        mongo.sales_control.insert_one(sale)

        # Vaciar carrito del usuario
        mongo.shopping_cart.delete_many({"id_user": id_user})

        return jsonify({"message": "Purchase completed successfully", "sale": sale}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
