from flask import Flask, request, jsonify
import json, shutil, requests, os

app = Flask(__name__)

port = 8000
CONFIGURE_PATH = ''
# DATA_NODES = {'3.137.174.40': '10.0.15.11'} #private: public
data_nodes = [5000, 5001, 5002, 5003]
available = data_nodes
down = []

@app.route('/', methods=['GET'])
def home():

    return '''
    <!doctype html>
    <title>Home</title>
    <h1>Hello! This is home page of name server.</h1>
    '''

@app.route('/get_ip', methods=['GET'])
def get_ip():
    global available
    check_available()
    if len(available) > 1:
        st = str(available[0])
        return st, 200

    return 'Not enough number of available servers. Data loss may occur', 400

# @app.route('/check_available', methods=['GET'])
def check_available():
    to_remove = []
    for node in available:
        try:
            res = requests.get('http://127.0.0.1:' + str(node) + '/')
        except requests.exceptions.ConnectionError:
            to_remove.append(node)
            down.append(node)

        else:
            if res.status_code != 200:
                to_remove.append(node)
                down.append(node)


    for node in to_remove:
        available.remove(node)

    to_remove = []

    for node in down:
        try:
            res = requests.get('http://127.0.0.1:' + str(node) + '/')
        except requests.exceptions.ConnectionError:
            pass
        else:
            if res.status_code == 200:
                update(node, available[0])
                available.append(node)
                to_remove.append(node)

    for node in to_remove:
        down.remove(node)



def update(node, av):
    data = {'ip': str(node)}
    response = requests.post("http://127.0.0.1:" + str(av) +
                             "/send_update", headers=data)

# @app.route('/replicate', methods=['POST'])
# def replicate():
#     global available
#
#     response = request.headers['ip']
#     print(available)
#     for node in available:
#
#         if not (str(node) == str(response)):
#             update(node, response)
#
#     return 'ok', 200

@app.route('/get_all_ip', methods=['GET'])
def all_av():
    resp = ''
    for node in available:
        resp += str(node) + ','

    return resp

if __name__ == '__main__':
    app.run(port=port)

