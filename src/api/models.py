from src.api.database import db

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120))

    def to_dict(self):
        return {'email': self.email, 'name': self.name}
