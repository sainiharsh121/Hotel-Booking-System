# app.py
from flask import Flask, request, jsonify
from models import db, User, Room, Booking
from config import Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
@app.route('/')
def home():
    return "✅ Hotel Booking System is running! " \
           "Visit /rooms to see available rooms."


@app.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.filter_by(is_available=True).all()
    return jsonify([{"id": r.id, "type": r.room_type, "price": r.price} for r in rooms])

@app.route('/book', methods=['POST'])
def book_room():
    data = request.json
    room = Room.query.get(data['room_id'])
    if room and room.is_available:
        booking = Booking(
            user_id=data['user_id'],
            room_id=data['room_id'],
            start_date=datetime.strptime(data['start_date'], "%Y-%m-%d"),
            end_date=datetime.strptime(data['end_date'], "%Y-%m-%d")
        )
        db.session.add(booking)
        room.is_available = False
        db.session.commit()
        return jsonify({"message": "Room booked successfully!"})
    return jsonify({"message": "Room not available"}), 400

@app.route('/bookings', methods=['GET'])
def all_bookings():
    bookings = Booking.query.all()
    return jsonify([
        {
            "id": b.id,
            "user_id": b.user_id,
            "room_id": b.room_id,
            "start_date": str(b.start_date),
            "end_date": str(b.end_date)
        } for b in bookings
    ])


@app.route('/cancel/<int:booking_id>', methods=['DELETE'])
def cancel_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if booking:
        room = Room.query.get(booking.room_id)
        room.is_available = True
        db.session.delete(booking)
        db.session.commit()
        return jsonify({"message": "Booking cancelled"})
    return jsonify({"message": "Booking not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
