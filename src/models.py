from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    active = db.Column(db.Boolean(), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "active": self.is_active
            # do not serialize the password, its a security breach
        }

    def check(self):
        return str(self.is_active())
    
    
    def update_user(self, response):
        for (key, value) in response.items():
            print(value)
            if hasattr(self, key):
                print(key)
                setattr(self, key, value)
        return True

    def is_authenticated(self):
        return True

    def is_active(self):
        return True
