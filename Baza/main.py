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
import numpy as np

#Начальная конфигурация
DATABASE = "tmp/nillbase.db"
DEBUG = True
SECRET_KEY = "312hbFNqld%1294"

main = Flask(__name__, template_folder="template")
main.config.from_object(__name__)

#Переопределение местоположения БД по адресу database/nillbase.db
main.config.update(dict(DATABASE = os.path.join(main.root_path, "database/nillbase.db")))

#Экземпляр класса flask_login
login_manager = LoginManager(main)
#Переадресация на авторизацию в случае непрохождения проверки login_required
login_manager.login_view = "loginning"
login_manager.login_message = "Access denied"

#Задание начальных значений переменных, передаваемых в index
Authorized = False
Username = ""

#Обработка функции UserLogin
@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, dbase)

#Соединение с базой данных
def connect_database():
    con = sqlite3.connect(main.config["DATABASE"])
    con.row_factory = sqlite3.Row
    return con

#Вспомогательная функция для создания начальной БД
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

#Функция соединения с БД, в случае, если оно не установлено
def get_db():
    if not hasattr(g, "link_db"):
        g.link_db = connect_database()
    return g.link_db

#Функция разрыва соединения с БД
@main.teardown_appcontext
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()


#ссылки на разные разделы
@main.route('/')
def index():
    #Проверка на обновление сессии браузера
    if current_user.is_authenticated and Authorized == False:
        logout_user()
    return render_template("first.html", Authorized = Authorized, Username = Username)


@main.route('/calculator')
def calculator():
    return render_template("calculator.html")
@main.route('/calculator_1.html')
def calc():
    return render_template("calculator_1.html")


main.register_blueprint(graf.bp)


@main.route('/3dfigures', methods = ("GET", "POST"))
#Необходиомсть авторизации
@login_required
def figures():
    if request.method == "POST":
        #Попытка построить фигуры при помощи try-except
        #Через фукнции из figures.py
        cylinder = ["", ""]
        pyramid = ["", ""]
        cubes = request.form.get("sizes1")
        error = None
        try:
            plot_url = fig.cube(int(cubes))
            return render_template("3dfigures.html", plot_url_1=plot_url)
        except:
            error = "Incorrect input data"
        balls = request.form.get("sizes2")
        try:
            plot_url = fig.ball(int(balls))
            return render_template("3dfigures.html", plot_url_2=plot_url)
        except:
            error = "Incorrect input data"
        pyramid[0] = request.form.get("sizes31")
        pyramid[1] = request.form.get("sizes32")
        try:
            plot_url = fig.pyramid(int(pyramid[0]), int(pyramid[1]))
            return render_template("3dfigures.html", plot_url_3=plot_url)
        except:
            error = "Incorrect input data"
        cylinder[0] = request.form.get("sizes41")
        cylinder[1] = request.form.get("sizes42")
        try:
            plot_url = fig.cylinder(int(cylinder[0]), int(cylinder[1]))
            return render_template("3dfigures.html", plot_url_4=plot_url)
        except:
            error = "Incorrect input data"

        #Вывод ошибки если входные данные не верны
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


@main.route('/physics')
@login_required
def inprogress2():
    return render_template("physics.html")
@main.route('/shary.html')
def shary():
    return render_template("shary.html")

@main.route('/matrix', methods=["POST","GET"])
@login_required
def matrix():
    if request.method == "POST":
        error = None
        try:
            row = request.form["input_row"]
            column = request.form["input_column"]
            inp_operation = request.form["inp_operation"]
            if inp_operation!="start":
                empty_matrix = [[0 for i in range(int(column))] for j in range(int(row))]
                for mr in range(int(row)):
                    for mc in range(int(column)):
                        matrix_string="matrix"+str(mr)+str(mc)
                        empty_matrix[mr][mc]=int(request.form[matrix_string])
                fm=np.matrix(empty_matrix)
                if inp_operation=="Select the operation!":
                    fm = np.squeeze(np.asarray(fm))
                    return render_template("matrix.html", row=range(int(row)),column=range(int(column)),inp_operation=inp_operation, fm=fm)
                if inp_operation=="Find determinant":
                    mat_det=round(np.linalg.det(fm))
                    fm = np.squeeze(np.asarray(fm))
                    return render_template("matrix.html", row=range(int(row)),column=range(int(column)),inp_operation=inp_operation, mat_det=mat_det, fm=fm)
                if inp_operation=="Find rank":
                    mat_det=round(np.linalg.matrix_rank(fm))
                    fm = np.squeeze(np.asarray(fm))
                    return render_template("matrix.html", row=range(int(row)),column=range(int(column)),inp_operation=inp_operation, mat_det=mat_det, fm=fm)
                if inp_operation in ["Transpose","Squaring","Find reverse"]:
                    if inp_operation=="Transpose":
                        row, column = column, row
                        fm=np.squeeze(np.asarray(fm.getT()))
                    if inp_operation=="Squaring":
                        fm=np.squeeze(np.asarray(np.matmul(fm, fm)))
                    if inp_operation=="Find reverse":
                        fm=np.squeeze(np.asarray(np.linalg.inv(fm)))
                    return render_template("matrix.html", row=range(int(row)),column=range(int(column)),inp_operation=inp_operation, fm=fm)

        except :
            error = "You can't use this matrix for this type of operation"
        if error is not None:
            flash(error)
            return render_template("matrix.html", row=range(int(row)),column=range(int(column)),inp_operation=inp_operation, err=error)
        return render_template("matrix.html", row=range(int(row)),column=range(int(column)),inp_operation=inp_operation)
    else:
        return render_template("matrix.html")


@main.route("/reg", methods = ("GET", "POST"))
def reg():
    if request.method == "POST":
        #Задание входных данных и вариантов возможных ошибок через массив
        errors = ["Passwords don't match",
                  "Invalid login (4 - 20) or password (5 - 20) length",
                  "The name cannot consist only numbers",
                  "This name is already registered"]
        excepted_chars = "*?!'^+%&;/()=}][{$#"
        name = request.form["login"]
        password = request.form["pass1"]
        passrepeat = request.form["pass2"]
        error = None
        #Проверки входных данных в формы регистрации на ошибки
        try:
            int(name)
        except:
            if 4 <= len(name) <= 20:
                for char in name:
                    if char in excepted_chars:
                        #Вывод ошибки вне массива, т.к. для нее необходим символ "char"
                        error = f"Invalid character {char}"
                if 5 <= len(password) <= 20:
                    if passrepeat == password:
                        #Конвертация пароля в hash
                        hash = generate_password_hash(password)
                        #Добавление пользователя в базу данных
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
    #Выход пользователя из аккаунта при нажатии кнопки "logout"
    logout_user()
    global Authorized
    Authorized = False
    return redirect(url_for("index"))


@main.route('/login', methods = ("GET", "POST"))
def loginning():
    #Проверка пользователя на авторизацию, если авторизован:
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    #Если нет:
    if request.method == "POST":
        #Получение данных о пользователе из базы данных
        user = dbase.GetUserByLogin(request.form["login"])
        if user and check_password_hash(user["pswrd"], request.form["pass"]):
            #Авторизация пользователя
            #Передача переменных в index для смены данных в шапке сайта
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            global Username
            Username = request.form["login"]
            global Authorized
            Authorized = True
            return redirect(url_for("index"))
        #Ошибка в случае ввода некорректных данных
        flash("Invalid Login or Password")

    return render_template("loginning.html")


@main.route('/about_us')
def aboutas():
    return render_template("about_us.html")


if __name__ == "__main__":
    main.run()