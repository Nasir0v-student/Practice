from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from extensions import db
import models

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

  
@app.route("/")
def index():
    return render_template("index.html", current_page="main")
@app.route("/films")
def films():
    films_list = models.Film.query.all()
    return render_template("films.html", films=films_list, current_page="films")
@app.route("/halls")
def halls():
    return render_template("halls.html", current_page="halls")
def main():
    app.run("0.0.0.0", port=5000, debug=True)
    


if __name__ == "__main__":
    main()