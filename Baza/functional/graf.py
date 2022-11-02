from distutils.log import error
from flask import (Blueprint, render_template, request, redirect, url_for, flash)
from sympy import Symbol, simplify
from numpy import arange


def create_graf(func, x_from, x_to):
    #функция для создания графика
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    #заданиее параметров графика
    x = Symbol('x')
    f = simplify(func)
    X = arange(x_from, x_to, 0.1)
    Y = list(map(lambda num: f.subs(x, num), X))
    #посторение графика функции
    plt.plot(X, Y)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    #сохранение графика функции в файлы сервера
    try:
        plt.savefig("static/img/2dgraf.png")
    except:
        plt.savefig("Baza/static/img/2dgraf.png")
    plt.close()


bp = Blueprint("2dgraf", __name__, url_prefix="/2dgraf")


#начальная страница с вводм функции для постоение графика
@bp.route("/function", methods = ("POST", "GET"))
def graf():
    if request.method == "POST":
        func = request.form["func"]
        x_from = request.form["xfrom"]
        x_to = request.form["xto"]
        #попытка построить график функции через try
        error = None
        try:
            create_graf(func, int(x_from), int(x_to))
        except:
            error = "Calculation error"
        else:
            return redirect(url_for("2dgraf.show_graf"))
        #вывод ошибки в случае ошибки
        if error is not None:
            flash(error)

    return render_template("2dgraf.html")


#страница с графиком предыдущей функции и возможностью задать новую
@bp.route("/img",  methods = ("POST", "GET"))
def show_graf():
    if request.method == "POST":
        func = request.form["func"]
        x_from = request.form["xfrom"]
        x_to = request.form["xto"]
        #попытка построить график функции через try
        error = None
        try:
            create_graf(func, int(x_from), int(x_to))
        except:
            error = "Calculation error"
        else:
            return render_template("2dgraf_img.html")
        #вывод ошибки в случае ошибки
        if error is not  None:
            flash(error)

    return render_template("2dgraf_img.html")


if __name__ == "__main__":
    f = 'sin(x)'
    create_graf(f, -5, 5)