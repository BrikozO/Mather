from flask import Flask, render_template, url_for, request, flash
import functional.Figures as fig
import functional.graf as graf
from sympy import symbols, integrate, diff, limit, simplify
main = Flask(__name__, template_folder="template")

main.secret_key = "dev"

#ссылки  на разные разделы
@main.route('/')
def index():
    return render_template("first.html")


@main.route('/calculator')
def calculator():
    return render_template("calculator.html")


main.register_blueprint(graf.bp)


@main.route('/3dfigures', methods = ("GET", "POST"))
def figures():
    if request.method == "POST":
        cylinder = ["", ""]
        pyramid = ["", ""]
        cubes = request.form.get("sizes1")
        try:
            plot_url = fig.cube(int(cubes))
            return render_template("3dfigures.html", plot_url_1=plot_url)
        except:
            print("error")
        balls = request.form.get("sizes2")
        try:
            plot_url = fig.ball(int(balls))
            return render_template("3dfigures.html", plot_url_2=plot_url)
        except:
            print("error")
        pyramid[0] = request.form.get("sizes31")
        pyramid[1] = request.form.get("sizes32")
        try:
            plot_url = fig.pyramid(int(pyramid[0]), int(pyramid[1]))
            return render_template("3dfigures.html", plot_url_3=plot_url)
        except:
            print("error")
        cylinder[0] = request.form.get("sizes41")
        cylinder[1] = request.form.get("sizes42")
        try:
            plot_url = fig.cylinder(int(cylinder[0]), int(cylinder[1]))
            return render_template("3dfigures.html", plot_url_4=plot_url)
        except:
            print("error")

    return render_template("3dfigures.html")

@main.route('/sympanents', methods=["POST","GET"])
def inprogress1():
    if request.method=="POST":
        fun= request.form["fun"]
        lim = request.form["lto"]
        symp=request.form["symp"]
        error = None
        try:
            fun=simplify(fun)
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
        return render_template("sympanents.html")



@main.route('/inprogress2')
def inprogress2():
    return render_template("inprogress2.html")


@main.route('/inprogress3')
def inprogress3():
    return render_template("inprogress3.html")


if __name__ == "__main__":
    main.run(debug=True)