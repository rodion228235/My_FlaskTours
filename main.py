import os

from flask import Flask, render_template, redirect, url_for, request
from dotenv import load_dotenv

from data import data




load_dotenv()

app = Flask(__name__)
app.secret_key = binascii.hexlify(os.urandom(24))
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_URI")
db.init_app(app)


with app.app_context():
    data_to_db()
#     db.create_all()


@app.context_processor
def 
    tours = {tour_id: tour for tour_id, tour in data.tours.items() if tour["departure"] == dep_eng}
    
    # tours = {}
    # for tour_id, tour in data.tours.items():
    #     if tour["departure"] == dep_eng:
    #         tours.update({tour_id: tour})
    
    return render_template("departure.html", tours=tours, dep_eng=dep_eng)


@app.get("/tour/<int:tour_id>/")
def get_tour(tour_id):
    tour = data.tours.get(tour_id)
    return render_template("tour.html", tour_id=tour_id, tour=tour)


@app.get("/buy_tour/<int:tour_id>/")
def buy_tour(tour_id):
    tour = data.tours.get(tour_id)
    return f"Ви успішно купили тур '{tour['title']}'. Дякуємо."


if __name__ == "__main__":
    app.run(debug=True)
