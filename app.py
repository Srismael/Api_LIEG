from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId

# Inicializar la aplicación Flask
app = Flask(__name__)

# Conectar a MongoDB Atlas
client = MongoClient("mongodb+srv://ismael:taco1234@cluster0.axu9d.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['LIEG']

# Rutas para la colección "product"
@app.route('/products', methods=['GET'])
def get_products():
    products = db.product.find()
    result = []
    for product in products:
        product['_id'] = str(product['_id'])
        result.append(product)
    return jsonify(result)

@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = db.product.find_one({"_id": ObjectId(id)})
    if product:
        product['_id'] = str(product['_id'])
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

@app.route('/product', methods=['POST'])
def add_product():
    data = request.json
    db.product.insert_one(data)
    return jsonify({"message": "Product added successfully!"}), 201

@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    data = request.json
    db.product.update_one({"_id": ObjectId(id)}, {"$set": data})
    return jsonify({"message": "Product updated successfully!"})

@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    db.product.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Product deleted successfully!"})

# Rutas para la colección "sales_control"
@app.route('/sales', methods=['GET'])
def get_sales():
    sales = db.sales_control.find()
    result = []
    for sale in sales:
        sale['_id'] = str(sale['_id'])
        result.append(sale)
    return jsonify(result)

@app.route('/sale/<id>', methods=['GET'])
def get_sale(id):
    sale = db.sales_control.find_one({"_id": ObjectId(id)})
    if sale:
        sale['_id'] = str(sale['_id'])
        return jsonify(sale)
    return jsonify({"error": "Sale not found"}), 404

@app.route('/sale', methods=['POST'])
def add_sale():
    data = request.json
    db.sales_control.insert_one(data)
    return jsonify({"message": "Sale added successfully!"}), 201

# Rutas para la colección "shopping_cart"
@app.route('/shopping_carts', methods=['GET'])
def get_shopping_carts():
    carts = db.shopping_cart.find()
    result = []
    for cart in carts:
        cart['_id'] = str(cart['_id'])
        result.append(cart)
    return jsonify(result)

@app.route('/shopping_cart/<id>', methods=['GET'])
def get_shopping_cart(id):
    cart = db.shopping_cart.find_one({"_id": ObjectId(id)})
    if cart:
        cart['_id'] = str(cart['_id'])
        return jsonify(cart)
    return jsonify({"error": "Shopping cart not found"}), 404

# Rutas para la colección "users"
@app.route('/users', methods=['GET'])
def get_users():
    users = db.users.find()
    result = []
    for user in users:
        user['_id'] = str(user['_id'])
        result.append(user)
    return jsonify(result)

@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = db.users.find_one({"_id": ObjectId(id)})
    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/user', methods=['POST'])
def add_user():
    data = request.json
    db.users.insert_one(data)
    return jsonify({"message": "User added successfully!"}), 201

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
