import os
import binascii

from flask import Flask, render_template, redirect, url_for, request, flash
from dotenv import load_dotenv
from flask_login import current_user, LoginManager, login_required, login_user, logout_user
from flask_migrate import Migrate

from data import data
from data.models import db, Tour, User
from data.tours_to_db import data_to_db
from data.forms import SignUpForm, LoginForm


load_dotenv()

app = Flask (__name__)
app.secret_key = binascii.hexlify(os.urandom(24))
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_URI")
db.init_app(app)
login_manager = LoginManager()
login_manager.login_message = "Для можливості бронювання увійдіть у систему" 
login_manager.login_view = "login"
login_manager.init_app(app)
migrate = Migrate(app, db)

# with app.app_context():
#     db.create_all()
#     data_to_db()


@app.context_processor
def global_data(): 
    return dict(
        title=data.title,
        departures=data.departures,
    )    


@login_manager.user_loader
def user_loader(user_id):
    return User.query.where(User.id==user_id).first()


@app.get("/")
def index():
    tours = Tour.query.all()
    return render_template("index.html", tours=tours)


@app.get("/departure/<dep_eng>/")
def departure(dep_eng):
    tours = Tour.query.where(Tour.departure==dep_eng).all()
    return render_template("departure.html", tours=tours, dep_eng=dep_eng)


@app.get("/tour/<int:tour_id>/")
def get_tour(tour_id):
    tour = Tour.query.where(Tour.id==tour_id).first_or_404()
    return render_template("tour.html", tour=tour)


@app.get("/buy_tour/<int:tour_id>/")
@login_required
def buy_tour(tour_id):
    tour = Tour.query.where(Tour.id==tour_id).first_or_404() 
    current_user.tours.append(tour)
    db.session.commit()
    flash("Ви успішно купили тур '{tour.title}'. Дякуємо.", "success") 
    return redirect(url_for("cabinet"))


@app.route("/signup/", methods=["GET", "POST"])
def signup():
    signup_form = SignUpForm()

    if signup_form.validate_on_submit(): 
        user = User(
            first_name=signup_form.first_name.data,
            last_name=signup_form.last_name.data,
            email=signup_form.email.data,
            password=signup_form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash("Успішно зареєстровано", "success") 
        return redirect(url_for("login"))
    
    return render_template("signup.html", form=signup_form)


@app.route("/login/", methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit(): 
        email = login_form.email.data
        password = login_form.password.data

        user = User.query.where(User.email==email).first()
        if user and user.is_validate_password(password):
            login_user(user)
            flash("Ви успішно увійшли", "success") 
            return redirect(url_for("cabinet"))
        else:
            flash("Логін або пароль не вірний", "error")
            return redirect(url_for("login"))
        
    return render_template("login.html", form=login_form)


@app.get("/cabinet/")
@login_required
def cabinet():
    return render_template("cabinet.html")


@app.get("/logout/")
@login_required
def logout():
    logout_user()
    flash("Ви успішно вийшли із системи", "success")
    return redirect(url_for("index"))


@app.get("/delete_tour/<int:tour_id>/")
@login_required
def delete_tour(tour_id):
    if current_user.is_admin:
       tour = Tour.query.where(Tour.id==tour_id).first_or_404()
       db.session.delete(tour)
       db.session.commit()
       flash(f"Typ з id '{id}' yсniшнo видалено", "success") 
       return redirect(url_for("index"))
    else:
       flash("Ви не можете видаляти записи")
       return redirect(url_for("index", "error"))
    

@app.get("/delete_tour_by_user/<int:tour_id>/")
@login_required
def delete_tour_by_user(tour_id):
    tour = Tour.query.where(Tour.id==tour_id).first_or_404()
    current_user.tours.remove(tour)
    db.session.commit()
    flash(f"Typ '{tour.title}' ycпiшно видалено", "success")
    return redirect(url_for("cabinet"))


if __name__ == "__main__":
    app.run(debug=True)
