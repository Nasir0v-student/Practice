from extensions import db

class Film(db.Model):
    __tablename__ = 'films'

    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(100), nullable=False)
   

    def __repr__(self):
        return f'<film {self.title}>'