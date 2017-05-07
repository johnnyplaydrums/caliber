from flask import Flask, render_template, request, jsonify

application = Flask(__name__)
application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@application.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@application.route("/get_data", methods=['GET'])
def get_data():
    return jsonify(result='success')

if __name__ == "__main__":
    application.run(host='0.0.0.0')
