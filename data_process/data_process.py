from flask import Flask, render_template, request, jsonify

application = Flask(__name__)
application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@application.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    application.run(host='0.0.0.0')
