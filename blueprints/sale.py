from flask import Blueprint, jsonify, request
from sqlalchemy.exc import NoResultFound, IntegrityError
from db import session, Sale
from datetime import datetime

from services.payment import payment_process

sale_bp = Blueprint("sale", __name__)


@sale_bp.route('/', methods=['GET', 'POST'])
def sales():
    if request.method == 'GET':
        return jsonify([sale.to_dict() for sale in session.query(Sale).all()]), 200
    elif request.method == 'POST':
        sale = request.get_json()
        try:
            session.add(Sale(
                client_id=sale['client_id'],
                sale_date=datetime.now(),
                total_price=0,
                payment_method=None,
                is_paid=False
            ))
            session.commit()
            return jsonify(sale), 201
        except IntegrityError:
            session.rollback()
            return jsonify({
                'error': 'Client not found'
            }), 404


@sale_bp.route('/<int:sale_id>', methods=['GET', 'PATCH', 'PUT', 'DELETE'])
def sale(sale_id):
    if request.method == 'GET':
        try:
            sale = session.query(Sale).filter(Sale.id == sale_id).one()
            return jsonify(sale.to_dict()), 200
        except NoResultFound:
            session.rollback()
            return jsonify({
                'error': 'Sale not found'
            }), 404

    elif request.method == 'PUT':
        sale = request.get_json()
        try:
            query = session.query(Sale).filter(Sale.id == sale_id)
            query.update({
                'client_id': sale['client_id'],
                'sale_date': sale['sale_date'],
                'total_price': sale['total_price'],
                'payment_method': sale['payment_method'],
                'is_paid': sale['is_paid']
            })
            sale = query.one().to_dict()
            session.commit()
            return jsonify(sale), 200
        except NoResultFound:
            session.rollback()
            return jsonify({
                'error': 'Sale not found'
            }), 404

    elif request.method == 'PATCH':
        sale = request.get_json()
        try:
            query = session.query(Sale).filter(Sale.id == sale_id)
            query.update(sale)
            sale = query.one().to_dict()
            session.commit()
            return jsonify(sale), 200
        except NoResultFound:
            session.rollback()
            return jsonify({
                'error': 'Sale not found'
            }), 404

    elif request.method == 'DELETE':
        try:
            query = session.query(Sale).filter(Sale.id == sale_id)
            sale = query.one().to_dict()
            query.delete()
            session.commit()
            return jsonify(sale), 200
        except NoResultFound:
            session.rollback()
            return jsonify({
                'error': 'Sale not found'
            }), 404
        except IntegrityError:
            session.rollback()
            return jsonify({
                'message': 'Sale contains products'
            }), 400

@sale_bp.route('/<int:sale_id>/payment', methods=['PATCH'])
def payment(sale_id):
    if request.method == 'PATCH':
        try:
            payment_method = request.get_json()['payment_method']
            query = session.query(Sale).filter(Sale.id == sale_id)
            request_sale = query.one().to_dict()
            request_json = {
                'sale_id': request_sale['id'],
                'is_paid': request_sale['is_paid'],
            }
            payment_process(request_json, payment_method)

            session.flush()
            updated_sale = query.one().to_dict()
            session.commit()
            return jsonify(updated_sale), 200

        except NoResultFound:
            session.rollback()
            return jsonify({
                'error': 'Sale not found'
            }), 404

