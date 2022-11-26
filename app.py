from flask import Flask, jsonify, request

app = Flask(__name__)

client_list = []


@app.route('/')
def hello_world():
    return '<h1> Hello World! </h1>'


@app.route('/api/v1/client', methods=['GET', 'POST'])
def contacts():
    if request.method == 'GET':
        return jsonify(client_list), 200
    elif request.method == 'POST':
        client = request.get_json()
        client_list.append(client)
        return jsonify(client_list), 201


@app.route('/api/v1/client/<int:client_id>', methods=['GET', 'PATCH', 'PUT', 'DELETE'])
def contact(client_id):
    response_client = None
    if request.method == 'GET':
        response_client = client_list[client_id]
    elif request.method == 'PUT':
        client = request.get_json()
        client_list[client_id] = client
        response_client = client
    elif request.method == 'PATCH':
        client = request.get_json()
        client_list[client_id].update(client)
        response_client = client
    elif request.method == 'DELETE':
        response_client = client_list[client_id]
        client_list.pop(client_id)
    return jsonify(response_client), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
