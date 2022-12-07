from flask import Blueprint, jsonify, request
from sqlalchemy.exc import NoResultFound
from db import session, ShoppingCart
from services.cart import decrease_stock, increase_total_price, increase_stock, decrease_total_price, \
    sum_sub_total_price

shopping_cart_bp = Blueprint('shopping_cart', __name__)

@shopping_cart_bp.route('/', methods=['GET', 'POST'])
def shopping_carts():
    if request.method == 'GET':
        return jsonify([cart.to_dict() for cart in session.query(ShoppingCart).all()]), 200
    elif request.method == 'POST':
        shopping_cart = request.get_json()
        try:
            decrease_stock(shopping_cart['product_id'], shopping_cart['quantity'])
            sub_total_price = sum_sub_total_price(shopping_cart['product_id'], shopping_cart['quantity'])
            increase_total_price(shopping_cart['sale_id'], sub_total_price)
            session.add(ShoppingCart(
                sale_id=shopping_cart['sale_id'],
                product_id=shopping_cart['product_id'],
                quantity=shopping_cart['quantity'],
                sub_total_price=sub_total_price
            ))
            session.commit()
            return jsonify(shopping_cart), 201
        except NoResultFound:
            session.rollback()
            return jsonify({'message': 'Product or Sale not found'}), 404
        except Exception as e:
            session.rollback()
            return jsonify({'message': str(e)}), 400


@shopping_cart_bp.route('/<int:shopping_cart_id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def shopping_cart(shopping_cart_id):
    if request.method == 'GET':
        try:
            return jsonify(session.query(ShoppingCart).filter(ShoppingCart.id == shopping_cart_id).one().to_dict()), 200
        except NoResultFound:
            session.rollback()
            return jsonify({'message': 'Shopping Cart not found'}), 404

    elif request.method == 'PUT':
        try:
            shopping_cart = session.query(ShoppingCart).filter(ShoppingCart.id == shopping_cart_id).one()
            cart_request = request.get_json()
            shopping_cart.sale_id = cart_request['sale_id']
            shopping_cart.product_id = cart_request['product_id']
            shopping_cart.quantity = cart_request['quantity']
            session.commit()
            return jsonify(shopping_cart.to_dict()), 200
        except NoResultFound:
            session.rollback()
            return jsonify({'message': 'Shopping Cart not found'}), 404

    elif request.method == 'PATCH':
        try:
            cart = request.get_json()
            query = session.query(ShoppingCart).filter(ShoppingCart.id == shopping_cart_id)
            query.update(cart)
            shopping_cart = query.one().to_dict()
            session.commit()
            return jsonify(shopping_cart.to_dict()), 200
        except NoResultFound:
            session.rollback()
            return jsonify({'message': 'Shopping Cart not found'}), 404

    elif request.method == 'DELETE':
        try:
            shopping_cart = session.query(ShoppingCart).filter(ShoppingCart.id == shopping_cart_id).one()
            increase_stock(shopping_cart.product_id, shopping_cart.quantity)
            decrease_total_price(shopping_cart.sale_id, shopping_cart.sub_total_price)
            session.delete(shopping_cart)
            session.commit()
            return jsonify(shopping_cart.to_dict()), 200
        except NoResultFound:
            session.rollback()
            return jsonify({'message': 'Shopping Cart not found'}), 404