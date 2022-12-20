import threading

from flask import Flask

from services.listener import listener
from blueprints.client import client_bp
from blueprints.product import product_bp
from blueprints.sale import sale_bp
from blueprints.shopping_cart import shopping_cart_bp

app = Flask(__name__)

app.register_blueprint(client_bp, url_prefix='/api/v1/client')
app.register_blueprint(product_bp, url_prefix='/api/v1/product')
app.register_blueprint(sale_bp, url_prefix='/api/v1/sale')
app.register_blueprint(shopping_cart_bp, url_prefix='/api/v1/shopping_cart')

@app.route('/')
def hello_world():
    return '<h1> Hello World! </h1>'


if __name__ == '__main__':
    threading.Thread(target=listener).start()
    app.run(host="0.0.0.0", port=8080, debug=True)
