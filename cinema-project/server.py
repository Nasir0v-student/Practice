from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from extensions import db
import models

# Assuming you have a separate config.py file
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # Replace with your actual database URI
    SECRET_KEY = 'your_secret_key'  # Replace with a strong secret key
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Suppress a warning

# No need to import db and models from separate files initially.  Define them here or import after app creation.

app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy *after* creating the app
db = SQLAlchemy(app)

# Initialize Flask-Migrate *after* creating the app and db
migrate = Migrate(app, db)


# Define your models *after* creating the db object
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    film = db.Column(db.String(100), nullable=False)
    hall = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    tickets = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Book(film='{self.film}', hall='{self.hall}', time='{self.time}', tickets={self.tickets})"


@app.route('/session')
def books():
    books = Book.query.all()  # Use the Book model defined above
    return render_template('sessions.html', books=books)


@app.route('/session/add', methods=['POST', 'GET'])  # Allow GET for displaying the form
def add_session():
    if request.method == 'POST':
        book = Book(
            film=request.form['film'],
            hall=request.form['hall'],
            time=request.form['time'],
            tickets=int(request.form['tickets'])  # Convert tickets to integer
        )
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('books'))  # Redirect to the books route

    return render_template('add_session.html') # Render a form for adding sessions


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
