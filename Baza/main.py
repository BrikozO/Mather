from flask import Flask, render_template, url_for, request
import functional.Figures as fig
import functional.graf as graf

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
            return render_template("3dfigures.html", plot_url=plot_url)
        except:
            print("error")
        balls = request.form.get("sizes2")
        try:
            plot_url = fig.ball(int(balls))
            return render_template("3dfigures.html", plot_url=plot_url)
        except:
            print("error")
        pyramid[0] = request.form.get("sizes31")
        pyramid[1] = request.form.get("sizes32")
        try:
            plot_url = fig.pyramid(int(pyramid[0]), int(pyramid[1]))
            return render_template("3dfigures.html", plot_url=plot_url)
        except:
            print("error")
        cylinder[0] = request.form.get("sizes41")
        cylinder[1] = request.form.get("sizes42")
        try:
            plot_url = fig.cylinder(int(cylinder[0]), int(cylinder[1]))
            return render_template("3dfigures.html", plot_url=plot_url)
        except:
            print("error")

    return render_template("3dfigures.html")

@main.route('/inprogress1')
def inprogress1():
    return render_template("inprogress1.html")


@main.route('/inprogress2')
def inprogress2():
    return render_template("inprogress2.html")


@main.route('/inprogress3')
def inprogress3():
    return render_template("inprogress3.html")


if __name__ == "__main__":
    main.run(debug=True)