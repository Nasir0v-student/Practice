from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from extensions import db
import models

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route("/")
def index():
    return render_template("index.html", current_page="main")

@app.route("/films", methods=['GET', 'POST'])
def films():
    if request.method == 'POST':
        name = request.form['name']
        genre = request.form['genre']
        duration = request.form['duration']

        new_film = models.Film(name=name, genre=genre, duration=duration)
        db.session.add(new_film)
        db.session.commit()

        return redirect(url_for('films'))

    films_list = models.Film.query.all()
    return render_template("films.html", films=films_list, current_page="films")

@app.route("/films/delete/<int:film_id>", methods=['POST'])
def delete_film(film_id):
    film = models.Film.query.get_or_404(film_id)
    db.session.delete(film)
    db.session.commit()
    return redirect(url_for('films'))

@app.route("/halls", methods=['GET', 'POST'])
def halls():
    if request.method == 'POST':
        number = request.form['number']
        capacity = request.form['capacity']
        hall_type = request.form['type']

        new_hall = models.Halls(number=number, capacity=capacity, type=hall_type)
        db.session.add(new_hall)
        db.session.commit()

        return redirect(url_for('halls'))

    halls_list = models.Halls.query.all()
    return render_template("halls.html", current_page="halls", halls=halls_list)

@app.route("/halls/delete/<int:hall_number>", methods=['POST'])
def delete_hall(hall_number):
    hall = models.Halls.query.filter_by(number=hall_number).first_or_404()
    db.session.delete(hall)
    db.session.commit()
    return redirect(url_for('halls'))

def main():
    with app.app_context():
        db.create_all()

        # Добавим начальные записи для фильмов
        if not models.Film.query.first():
            film1 = models.Film(name="Начало", genre="Фантастика", duration="148 минут")
            film2 = models.Film(name="Интерстеллар", genre="Приключения", duration="169 минут")
            film3 = models.Film(name="Матрица", genre="Экшн", duration="136 минут")
            db.session.add_all([film1, film2, film3])
            db.session.commit()

        # Добавим начальные записи для залов
        if not models.Halls.query.first():
            hall1 = models.Halls(number=1, capacity=100, type="Большой")
            hall2 = models.Halls(number=2, capacity=60, type="Средний")
            hall3 = models.Halls(number=3, capacity=30, type="Малый")
            db.session.add_all([hall1, hall2, hall3])
            db.session.commit()

    app.run("0.0.0.0", port=5000, debug=True)
    

if __name__ == "__main__":
    main()
