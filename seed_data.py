from app import app, db
from models import Room

with app.app_context():
    rooms = [
        Room(room_type='Single', price=1000.0),
        Room(room_type='Double', price=1500.0),
        Room(room_type='Suite', price=2500.0),
        Room(room_type='Deluxe', price=3000.0),
        Room(room_type='Family', price=3500.0),
        Room(room_type='Luxury Suite', price=5000.0),
    ]
    db.session.bulk_save_objects(rooms)
    db.session.commit()
    print("✅ Sample rooms added!")
