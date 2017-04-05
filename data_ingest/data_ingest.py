from flask import Flask, render_template, request, jsonify
application = Flask(__name__)
application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@application.route("/")
def hello():
    return render_template('index.html')

@application.route("/data", methods=["POST"])
def data_ingest():
    print('X DATA', request.get_json()['x_data'][0:10])
    print('Y DATA', request.get_json()['y_data'][0:10])
    print('Z DATA', request.get_json()['z_data'][0:10])
    # print('LAT DATA', request.get_json()['lat_data'][0:10])
    # print('LONG DATA', request.get_json()['long_data'][0:10])
    return jsonify(result="success")

@application.route("/get_data", methods=["GET"])
def get_data():
    print('get_data')
    return jsonify(x_data=x_data)

if __name__ == "__main__":
    application.run(host='0.0.0.0')
