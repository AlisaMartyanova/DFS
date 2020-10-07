from flask import Flask, request, jsonify
import json, shutil, requests, os

app = Flask(__name__)

port = 5550
CONFIGURE_PATH = ''

s1 = os.environ["STORAGE_1_HOST"] + ":" + os.environ["STORAGE_1_PORT"]
s2 = os.environ["STORAGE_2_HOST"] + ":" + os.environ["STORAGE_2_PORT"]
s3 = os.environ["STORAGE_3_HOST"] + ":" + os.environ["STORAGE_3_PORT"]
s1_pub = os.environ["S1_PUB_H"] + ":" + os.environ["S1_PUB_PORT"]
s2_pub = os.environ["S2_PUB_H"] + ":" + os.environ["S2_PUB_PORT"]
s3_pub = os.environ["S3_PUB_H"] + ":" + os.environ["S3_PUB_PORT"]
data_nodes = [s1, s2, s3]
ips = {s1:s1_pub, s2:s2_pub, s3:s3_pub}
available = data_nodes
down = []

@app.route('/', methods=['GET'])
def home():

    return '''
    <!doctype html>
    <title>Home</title>
    <h1>Hello! This is home page of name server.</h1>
    '''


#send ip of available data server to client 
@app.route('/get_ip', methods=['GET'])
def get_ip():
    global available
    check_available()
    if len(available) > 1:
        st = str(ips[available[0]])
        return st, 200

    return 'Not enough number of available servers. Data loss may occur', 400

#check which servers are available 
def check_available():
    to_remove = []
    for node in available:
        try:
            res = requests.get('http://' + str(node) + '/')
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
            res = requests.get('http://' + str(node) + '/')
        except requests.exceptions.ConnectionError:
            pass
        else:
            if res.status_code == 200:
                update(node, available[0])
                available.append(node)
                to_remove.append(node)

    for node in to_remove:
        down.remove(node)


#update servers that was down
def update(node, av):
    data = {'ip': str(node)}
    response = requests.post("http://" + str(av) +
                             "/send_update", headers=data)


#send ip of all available servers to server that executes client command
@app.route('/get_all_ip', methods=['GET'])
def all_av():
    resp = ''
    for node in available:
        resp += str(node) + ','

    return resp

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)

