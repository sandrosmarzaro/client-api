from flask import Flask, jsonify, request
from sqlalchemy.exc import NoResultFound

from db import session, Client

app = Flask(__name__)


@app.route('/')
def hello_world():
    return '<h1> Hello World! </h1>'


@app.route('/api/v1/client', methods=['GET', 'POST'])
def clients():
    if request.method == 'GET':
        return jsonify([client.to_dict() for client in session.query(Client).all()]), 200
    elif request.method == 'POST':
        client = request.get_json()
        session.add(Client(
            name=client['name'],
            birth_date=client['birth_date']
        ))
        session.commit()
        return jsonify(client), 201


@app.route('/api/v1/client/<int:client_id>', methods=['GET', 'PATCH', 'PUT', 'DELETE'])
def contact(client_id):

    if request.method == 'GET':
        try:
            client = session.query(Client).filter(Client.id == client_id).one()
            return jsonify(client.to_dict()), 200
        except NoResultFound:
            return jsonify({
                'message': 'Client not found'
            }), 404

    elif request.method == 'PUT':
        client = request.get_json()
        try:
            query = session.query(Client).filter(Client.id == client_id)
            query.update({
                'name': client['name'],
                'birth_date': client['birth_date']
            })
            client = query.one().to_dict()
            session.commit()
            return jsonify(client), 200
        except NoResultFound:
            return jsonify({
                'message': 'Client not found'
            }), 404

    elif request.method == 'PATCH':
        client = request.get_json()
        try:
            query = session.query(Client).filter(Client.id == client_id)
            query.update(client)
            client = query.one().to_dict()
            session.commit()
            return jsonify(client), 200
        except NoResultFound:
            return jsonify({
                'message': 'Client not found'
            }), 404

    elif request.method == 'DELETE':
        try:
            query = session.query(Client).filter(Client.id == client_id)
            client = query.one().to_dict()
            query.delete()
            session.commit()
            return jsonify(client), 200
        except NoResultFound:
            return jsonify({
                'message': 'Client not found'
            }), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
