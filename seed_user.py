# seed_user.py
from app import app
from models import db, User

with app.app_context():
    user = User(name="Harsh Saini", email="harsh@example.com")
    db.session.add(user)
    db.session.commit()
    print("✅ Sample user created!")
