import requests
from flask import Flask, render_template, request, jsonify
from utils.process_data import process_data

application = Flask(__name__)
application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@application.route("/")
def hello():
    return render_template('index.html')

@application.route("/data", methods=["POST"])
def data_ingest(data):
    data = request.get_json()
    keys = process_data(data)
    req = requests.post('http://34.205.34.72/new_data', json=keys)
    return jsonify(result="success")

@application.route("/get_data", methods=["GET"])
def get_data():
    print('get_data')
    return jsonify(x_data=x_data)

if __name__ == "__main__":
    application.run(host='0.0.0.0')
