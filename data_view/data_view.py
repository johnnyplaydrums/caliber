from flask import Flask, render_template, request, jsonify
from utils.get_data import get_recent, get_worst

application = Flask(__name__)
application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@application.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@application.route('/get_data', methods=['GET'])
def get_data():
    recent = get_recent()
    worst = get_worst()
    return jsonify(recent=recent, worst=worst)

@application.route('/map')
def map():
    return render_template('map.html')


if __name__ == "__main__":
    application.run(host='0.0.0.0')
