from distutils.log import error
from flask import (Blueprint, render_template, request, redirect, url_for, flash)
from sympy import Symbol, simplify
from numpy import arange

def create_graf(func, x_from, x_to):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    x = Symbol('x')
    f = simplify(func)
    X = arange(x_from, x_to, 0.1)
    Y = list(map(lambda num: f.subs(x, num), X))
    plt.plot(X, Y)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.savefig("Baza/static/img/2dgraf.png")
    plt.close()


bp = Blueprint("2dgraf", __name__, url_prefix="/2dgraf")


@bp.route("/function"  , methods = ("POST", "GET"))
def graf():
    if request.method == "POST":
        func = request.form["func"]
        x_from = request.form["xfrom"]
        x_to = request.form["xto"]
        error = None
        try:
            create_graf(func, int(x_from), int(x_to))
        except:
            error = "You, stupid bastard, cannot enter valid value to range of x!"
        else:
            return redirect(url_for("2dgraf.show_graf"))

        if error is not None:
            flash(error)

    return render_template("2dgraf.html")


@bp.route("/img",  methods = ("POST", "GET"))
def show_graf():
    if request.method == "POST":
        func = request.form["func"]
        x_from = request.form["xfrom"]
        x_to = request.form["xto"]
        error = None
        try:
            create_graf(func, int(x_from), int(x_to))
        except:
            error = "You, stupid bastard, cannot enter valid function or range of x!"
        else:
            return render_template("2dgraf_img.html")
        
        if error is not  None:
            flash(error)

    return render_template("2dgraf_img.html")

if __name__ == "__main__":
    f = 'sin(x)*tan(x) - x4'
    create_graf(f, -5, 5)