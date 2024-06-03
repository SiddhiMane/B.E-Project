from math import atan2, cos, radians, sin, sqrt
from uuid import uuid1

from db import Database
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)
CORS(app)
db = Database()

parking_spots = [
    {
        "name": "Ajay Parking Arena",
        "coordinates": [18.574463634619526, 73.97850036621095],
        "cost": 60,
        "slots_available": 4,
        "distance": "50m"
    },
    {
        "name": "Vaishnavi Parking Arena",
        "coordinates": [18.58070537898126, 73.98033499717714],
        "cost": 100,
        "slots_available": 4,
        "distance": "50m"
    },
    {
        "name": "Siddhi Parking Arena",
        "coordinates": [18.5791665231974, 73.97450923919679],
        "cost": 500,
        "slots_available": 4,
        "distance": "50m"
    },
    {
        "name": "Sunny Parking Arena",
        "coordinates": [18.57598341060873, 73.96438121795656],
        "cost": 1000,
        "slots_available": 4,
        "distance": "50m"
    },
    {
        "name": "CaptainMeow Parking Arena",
        "coordinates": [18.58020205447126, 73.99011969566347],
        "cost": 5000,
        "slots_available": 4,
        "distance": "50m"
    },
]

def calculate_distance(coord1, coord2):
    R = 6371.0

    lat1 = radians(coord1[0])
    lon1 = radians(coord1[1])
    lat2 = radians(coord2[0])
    lon2 = radians(coord2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

# Completed Not Tested
class ParkingInfo(Resource):
    def get(self):
        city = request.args.get('city')
        lat = request.args.get('latitude')
        lon = request.args.get('latitude')
        coordinates = [float(lat), float(lon)]
        
        data_array = db.getAllValues()
        if len(data_array) == 0:
            return jsonify(parking_spots)
        filtered_data = [d for d in data_array if d['city'] == city]
        filtered_data.sort(key=lambda x: calculate_distance(x['coordinates'], coordinates))
        
        top_5_nearby = filtered_data[:5]

        return jsonify(parking_spots)


class UpdateDB(Resource):
    def get(self):
        uuid = request.args.get('uuid')
        slots_available = request.args.get('slots_available')
        try:
            res = db.set(uuid, slots_available)
        except Exception as err:
            print(f"An exception occured while updating the database. Hint: {err}")
        if res:
            return {"status": "success"}
        return {"status": "failure"}


class RegisterParkingToDB(Resource):
    def post(self):
        data = request.form.to_dict()
        print("Data Received :", data)
        uuid = str(uuid1())
        data = {
            'uuid': uuid,
            'owner_name': data['name'],
            'city': data['city'],
            'name': data['parkingname'],
            'parkingaddress': data['parkingaddress'],
            'phoneno': data['phonenumber'],
            'coordinates': [float(data['latitude']) , float(data['longitude'])],
            'cost': data['cost'],
            'total_slots': data['parkingspots'],
            'slots_available': data['parkingspots'],
            'distance': '50m' 
        }
        res = db.insert(uuid, data)
        res = True
        if res:
            return {'status': 'success'}, 200
        return {'status': 'failure'}, 200

api.add_resource(ParkingInfo, '/api/v1/get_parking_info')
api.add_resource(UpdateDB, '/api/v1/update_parking_info')
api.add_resource(RegisterParkingToDB, '/api/v1/register_parking')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
