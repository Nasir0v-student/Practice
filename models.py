from extensions import db

class Halls(db.Model):
    __tablename__ = 'halls'

    number = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Halls {self.title}>'