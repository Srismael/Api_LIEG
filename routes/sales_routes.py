from flask import Blueprint, jsonify, request
from bson import ObjectId
from config import mongo

sales_bp = Blueprint('sales', __name__)

# Función auxiliar para convertir ObjectId a string
def convert_objectid_to_str(sale):
    sale['_id'] = str(sale['_id'])  # Convertir _id a string
    # Si hay otros campos con ObjectId, también conviértelos a string aquí si es necesario
    return sale

# Obtener todas las ventas
@sales_bp.route('/sales', methods=['GET'])
def get_sales():
    sales = mongo.sales_control.find()
    result = [convert_objectid_to_str(sale) for sale in sales]
    return jsonify(result)
