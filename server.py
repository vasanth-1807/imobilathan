from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicle_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model for vehicle data
class VehicleData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    speed = db.Column(db.Float, nullable=False)
    road_condition = db.Column(db.String(50), nullable=False)
    weather = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/send_data', methods=['POST'])
def receive_data():
    data = request.json
    vehicle_data = VehicleData(
        vehicle_id=data['vehicle_id'],
        location=data['location'],
        speed=data['speed'],
        road_condition=data['road_condition'],
        weather=data['weather'],
        timestamp=datetime.fromtimestamp(data['timestamp'])
    )
    db.session.add(vehicle_data)
    db.session.commit()
    return jsonify({"status": "Data received"}), 200

@app.route('/get_data', methods=['GET'])
def get_data():
    vehicle_data_records = VehicleData.query.all()
    data_list = [
        {
            "vehicle_id": record.vehicle_id,
            "location": record.location,
            "speed": record.speed,
            "road_condition": record.road_condition,
            "weather": record.weather,
            "timestamp": record.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
        for record in vehicle_data_records
    ]
    return jsonify(data_list), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
