from flask import Flask, render_template, url_for, request, flash, redirect, g
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from functional.AddDataBase import AddDataBase
from functional.UserLogin import UserLogin
from werkzeug.security import generate_password_hash, check_password_hash
import functional.Figures as fig
import functional.graf as graf
import os
import sqlite3
from sympy import symbols, integrate, diff, limit, simplify


DATABASE = "tmp/nillbase.db"
DEBUG = True
SECRET_KEY = "312hbFNqld%1294"

main = Flask(__name__, template_folder="template")
main.config.from_object(__name__)

main.config.update(dict(DATABASE = os.path.join(main.root_path, "database/nillbase.db")))


login_manager = LoginManager(main)
login_manager.login_view = "loginning"
login_manager.login_message = "Access denied"


Authorized = False
Username = ""


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, dbase)


def connect_database():
    con = sqlite3.connect(main.config["DATABASE"])
    con.row_factory = sqlite3.Row
    return con


def create_db():
    db = connect_database()
    with main.open_resource("database/sq_db.sql", mode = "r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


dbase = None
@main.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = AddDataBase(db)


def get_db():
    if not hasattr(g, "link_db"):
        g.link_db = connect_database()
    return g.link_db


@main.teardown_request
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()


#ссылки  на разные разделы
@main.route('/')
def index():
    return render_template("first.html", Authorized = Authorized, Username = Username)


@main.route('/calculator')
def calculator():
    return render_template("calculator.html")
@main.route('/calculator_1.html')
def calc():
    return render_template("calculator_1.html")


main.register_blueprint(graf.bp)


@main.route('/3dfigures', methods = ("GET", "POST"))
@login_required
def figures():
    if request.method == "POST":
        cylinder = ["", ""]
        pyramid = ["", ""]
        cubes = request.form.get("sizes1")
        error = None
        try:
            plot_url = fig.cube(int(cubes))
            return render_template("3dfigures.html", plot_url_1=plot_url)
        except:
            error = "Неверные входные данные"
        balls = request.form.get("sizes2")
        try:
            plot_url = fig.ball(int(balls))
            return render_template("3dfigures.html", plot_url_2=plot_url)
        except:
            error = "Неверные входные данные"
        pyramid[0] = request.form.get("sizes31")
        pyramid[1] = request.form.get("sizes32")
        try:
            plot_url = fig.pyramid(int(pyramid[0]), int(pyramid[1]))
            return render_template("3dfigures.html", plot_url_3=plot_url)
        except:
            error = "Неверные входные данные"
        cylinder[0] = request.form.get("sizes41")
        cylinder[1] = request.form.get("sizes42")
        try:
            plot_url = fig.cylinder(int(cylinder[0]), int(cylinder[1]))
            return render_template("3dfigures.html", plot_url_4=plot_url)
        except:
            error = "Неверные входные данные"

        if error is not None:
            flash(error)
            return render_template("3dfigures.html")

    return render_template("3dfigures.html")


@main.route('/sympanents', methods=["POST","GET"])
@login_required
def sympanents():
    if request.method=="POST":
        fun = request.form["fun"]
        lim = request.form["lto"]
        symp = request.form["symp"]
        error = None
        if symp != "None":
            if any((symp == "Int", symp == "Dif")) and lim != "":
                flash("Invalid input parameters")
                return render_template("sympanents.html")
            else:
                try:
                    fun = simplify(fun)
                    x = symbols('x')
                    if symp == "Int":
                        ab=integrate(fun, x)
                    elif symp == "Dif":
                        ab=diff(fun, x)
                    elif symp == "Lim":
                        ab=limit(fun, x, lim)
                except:
                    error = "Calculation error"
                else:
                    return render_template("sympanents.html", abc=ab)
                if error is not None:
                    flash(error)
                    return render_template("sympanents.html")
        else:
            flash("Sympanent are not set")
            return render_template("sympanents.html")
    else:
        return render_template("sympanents.html")


@main.route('/inprogress2')
@login_required
def inprogress2():
    return render_template("inprogress2.html")
@main.route('/shary.html')
def shary():
    return render_template("shary.html")

@main.route('/inprogress3')
@login_required
def inprogress3():
    return render_template("inprogress3.html")


@main.route("/reg", methods = ("GET", "POST"))
def reg():
    if request.method == "POST":
        errors = ["Passwords don't match",
                  "Invalid login (4 - 20) or password (5 - 20) length",
                  "The name cannot consist only numbers",
                  "This name is already registered"]
        excepted_chars = "*?!'^+%&;/()=}][{$#"
        name = request.form["login"]
        password = request.form["pass1"]
        passrepeat = request.form["pass2"]
        error = None
        try:
            int(name)
        except:
            if 4 <= len(name) <= 20:
                for char in name:
                    if char in excepted_chars:
                        error = f"Invalid character {char}"
                if 5 <= len(password) <= 20:
                    if passrepeat == password:
                        hash = generate_password_hash(password)
                        res = dbase.AddUser(name, hash)
                        if res:
                            return redirect(url_for("loginning"))
                        else:
                            error = errors[3]
                    else:
                        error = errors[0]
                else:
                    error = errors[1]
            else:
                error = errors[1]
        else:
            error = errors[2]

        if error is not None:
            flash(error)
            return render_template("registration.html")

    return render_template("registration.html")

@main.route('/logout')
@login_required
def logout():
    logout_user()
    global Authorized
    Authorized = False
    return redirect(url_for("index"))


@main.route('/login', methods = ("GET", "POST"))
def loginning():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        user = dbase.GetUserByLogin(request.form["login"])
        if user and check_password_hash(user["pswrd"], request.form["pass"]):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            global Username
            Username = request.form["login"]
            global Authorized
            Authorized = True
            return redirect(url_for("index"))

        flash("Invalid Login or Password")

    return render_template("loginning.html")


@main.route('/about_us')
def aboutas():
    return render_template("about_us.html")


if __name__ == "__main__":
    main.run()