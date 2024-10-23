from flask import Flask
from pymongo import MongoClient
from routes.product_routes import product_bp
from routes.sales_routes import sales_bp
from routes.cart_routes import cart_bp
from routes.user_routes import user_bp
from config import mongo

app = Flask(__name__)

# Registrar Blueprints para modularización
app.register_blueprint(product_bp)
app.register_blueprint(sales_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(user_bp)


# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
