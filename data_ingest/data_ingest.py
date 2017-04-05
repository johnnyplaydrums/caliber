from flask import Flask, render_template, request, jsonify
application = Flask(__name__)
application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
x_data = [];

@application.route("/")
def hello():
    return render_template('index.html')

@application.route("/data", methods=["POST"])
def data_ingest():
    print(request.get_json()['x_data'])
    x_data = request.get_json()['x_data']
    return jsonify(result="success")

@application.route("/get_data", methods=["GET"])
def get_data():
    print('get_data')
    return jsonify(x_data=x_data)

if __name__ == "__main__":
    application.run(host='0.0.0.0')
