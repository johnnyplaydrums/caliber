import geocoder, math
from flask import Flask, render_template, request, jsonify
from views.send_to_redshift import send_to_redshift

application = Flask(__name__)
application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@application.route("/")
def hello():
    return render_template('index.html')

@application.route("/data", methods=["POST"])
def data_ingest():
    data = request.get_json()
    address_points = {}

    last_point = (0,0)
    for index in range(len(data['lat'])):
        current_point = (data['lat'][index], data['long'][index])
        if last_point != current_point:
            print(last_point, current_point)
            address = geocoder.google([current_point[0], current_point[1]], method='reverse')
            last_address = str(int(math.ceil(int(address.address.split(' ', 1)[0]) / 100) * 100)) + ' ' + address.address.split(' ', 1)[1]
            if last_address in address_points:
                address_points[last_address]['lat'].append(current_point[0])
                address_points[last_address]['long'].append(current_point[1])
                address_points[last_address]['x'].append(data['x'][index])
                address_points[last_address]['y'].append(data['y'][index])
                address_points[last_address]['z'].append(data['z'][index])
            else:
                address_points[last_address] = {
                    'lat': [current_point[0]],
                    'long': [current_point[1]],
                    'x': [data['x'][index]],
                    'y': [data['y'][index]],
                    'z': [data['z'][index]],
                    'processed': 'false'
                }

            last_point = current_point
            print(last_address)
        else:
            address_points[last_address]['lat'].append(current_point[0])
            address_points[last_address]['long'].append(current_point[1])
            address_points[last_address]['x'].append(data['x'][index])
            address_points[last_address]['y'].append(data['y'][index])
            address_points[last_address]['z'].append(data['z'][index])

    send_to_redshift(address_points)
    return jsonify(result="success")

@application.route("/get_data", methods=["GET"])
def get_data():
    print('get_data')
    return jsonify(x_data=x_data)

if __name__ == "__main__":
    application.run(host='0.0.0.0')
