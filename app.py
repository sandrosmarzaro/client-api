from flask import Flask

from blueprints.client import client_bp
from blueprints.product import product_bp

app = Flask(__name__)

app.register_blueprint(client_bp, url_prefix='/api/v1/client')
app.register_blueprint(product_bp, url_prefix='/api/v1/product')


@app.route('/')
def hello_world():
    return '<h1> Hello World! </h1>'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
