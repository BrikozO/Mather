from flask import Flask, render_template, url_for


main = Flask(__name__, template_folder="template")

main.secret_key = "dev"

#ссылки  на разные разделы
@main.route('/')
def index():
    return render_template("first.html")


@main.route('/calculator')
def calculator():
    return render_template("calculator.html")


import functional.graf as graf
main.register_blueprint(graf.bp)


@main.route('/3dfigures')
def figures():
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