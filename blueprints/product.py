from flask import Blueprint, jsonify, request
from sqlalchemy.exc import NoResultFound, IntegrityError

from db import session, Product

product_bp = Blueprint('product', __name__)

@product_bp.route('/', methods=['GET', 'POST'])
def products():
    if request.method == 'GET':
        return jsonify([product.to_dict() for product in session.query(Product).all()]), 200
    elif request.method == 'POST':
        product = request.get_json()
        session.add(Product(
            name=product['name'],
            price=product['price'],
            inventory=product['inventory']
        ))
        session.commit()
        return jsonify(product), 201

@product_bp.route('/<int:product_id>', methods=['GET', 'PATCH', 'PUT', 'DELETE'])
def product(product_id):
    if request.method == 'GET':
        try:
            product = session.query(Product).filter(Product.id == product_id).one()
            return jsonify(product.to_dict()), 200
        except NoResultFound:
            session.rollback()
            return jsonify({
                'message': 'Product not found'
            }), 404

    elif request.method == 'PUT':
        product = request.get_json()
        try:
            query = session.query(Product).filter(Product.id == product_id)
            query.update({
                'name': product['name'],
                'price': product['price'],
                'inventory': product['inventory']
            })
            product = query.one().to_dict()
            session.commit()
            return jsonify(product), 200
        except NoResultFound:
            session.rollback()
            return jsonify({
                'message': 'Product not found'
            }), 404

    elif request.method == 'PATCH':
        product = request.get_json()
        try:
            query = session.query(Product).filter(Product.id == product_id)
            query.update(product)
            product = query.one().to_dict()
            session.commit()
            return jsonify(product), 200
        except NoResultFound:
            session.rollback()
            return jsonify({
                'message': 'Product not found'
            }), 404

    elif request.method == 'DELETE':
        try:
            query = session.query(Product).filter(Product.id == product_id)
            product = query.one().to_dict()
            query.delete()
            session.commit()
            return jsonify(product), 200
        except NoResultFound:
            session.rollback()
            return jsonify({
                'message': 'Product not found'
            }), 404
        except IntegrityError:
            session.rollback()
            return jsonify({
                'message': 'Product is associated with a sale'
            }), 400
