from flask import Flask, render_template, request, jsonify
from utils.process_data import process_data

application = Flask(__name__)
application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@application.route("/new_data", methods=['POST'])
def index():
    data = request.get_json()
    process_data(data)
    return jsonify(result='success')
    
if __name__ == "__main__":
    application.run(host='0.0.0.0')
