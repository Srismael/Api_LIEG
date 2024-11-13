from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import mongo, JWT_SECRET_KEY
from routes.product_routes import product_bp
from routes.sales_routes import sales_bp
from routes.cart_routes import cart_bp
from routes.user_routes import user_bp
from routes.auth_routes import auth_bp  # Importa el nuevo blueprint de autenticación

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
jwt = JWTManager(app)

# Registrar Blueprints
app.register_blueprint(product_bp)
app.register_blueprint(sales_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(user_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')  # Registrar auth con prefijo

if __name__ == '__main__':
    app.run(debug=True)
