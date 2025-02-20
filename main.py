from textwrap import dedent

from flask import Flask, request, render_template, url_for, redirect, session
from flask_session import Session
import services.math_service as math_service
from tests.test import insert_customer, login_customer

app = Flask(__name__, static_url_path='/static', static_folder='static')

app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "supersecretkey"
Session(app)

languages = [
    {"name": "Python", "creator": "Guido van Rossum", "year": 1991},
    {"name": "JavaScript", "creator": "Brendan Eich", "year": 1995},
    {"name": "Java", "creator": "James Gosling", "year": 1995},
    {"name": "C#", "creator": "Microsoft", "year": 2000},
    {"name": "Ruby", "creator": "Yukihiro Matsumoto", "year": 1995},
]


@app.route("/")
def home() -> str:
    print(math_service.add(1.0, 2.0))
    app.logger.info("Rendering home page")
    return render_template("home.html")


@app.route("/about_flask")
def about_flask() -> str:
    app.logger.info("Rendering About Flask page")
    return render_template("about_flask.html")


@app.route("/contact")
def contact() -> str:
    return render_template("contact.html")


@app.route("/profile")
def profile() -> str:
    return render_template("profile.html")


@app.route("/submit", methods=["POST"])
def submit():
    firstname = request.form.get("firstname")
    surname = request.form.get("surname")
    email = request.form.get("email")
    password = request.form.get("password")
    birthdate = request.form.get("birthdate")

    session['firstname'] = firstname
    session['surname'] = surname
    session['email'] = email
    session['password'] = password
    session['birthdate'] = birthdate

    if insert_customer(firstname, surname, email, password, birthdate):
        print("ja")
        return render_template("erfolg_registriert.html", surname=surname, firstname='Hallo ' + firstname)
    else:
        print("nai")
        return render_template('falsch_registriert.html', surname='Die Email wurde schon registriert.')

@app.route("/submit2", methods=["POST"])
def submit2():
    email = request.form.get("email")
    password = request.form.get("password")

    session['email'] = email
    session['password'] = password

    if login_customer(email, password):
        print("ja")
        return render_template("erfolg_registriert.html", surname='Erfolgreich angemeldet!')
    else:
        print("nai")
        return render_template('falsch_registriert.html', surname='Email und/oder Passwort stimmt nicht!')

@app.route("/login")
def login() -> str:
    return render_template("login.html")


@app.route("/deleteaccount")
def deleteaccount() -> str:
    return render_template("deleteaccount.html")


@app.route("/warenkorb")
def cart():
    cart_items = session.get("cart", [])

    subtotal = sum(float(item["price"].replace(" CHF", "").strip()) for item in cart_items) if cart_items else 0.0
    total = round(subtotal, 2)

    return render_template("cart.html", cart_items=cart_items, subtotal=subtotal, total=total)


@app.route("/shop")
def shop() -> str:
    return render_template("shop.html")


@app.route("/visa")
def visa() -> str:
    return render_template("visa.html")


@app.route('/bestellbestaetigung')
def bestellbestaetigung():
    return render_template("bestellbestaetigung.html")


@app.route("/paypal")
def paypal() -> str:
    return render_template("paypal.html")


@app.route("/paypalzahlungsbildschirm")
def paypalzahlungsbildschirm() -> str:
    return render_template("paypalZahlungsbildschirm.html")


@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    product_name = request.form.get("product_name")
    product_image = request.form.get("product_image")
    product_price = request.form.get("product_price")

    cart = session.get("cart", [])
    cart.append({"name": product_name, "image": product_image, "price": product_price})
    session["cart"] = cart
    session["cart_count"] = len(cart)

    return redirect(url_for("shop"))



@app.route("/clear_cart")
def clear_cart():
    session.pop("cart", None)
    session["cart_count"] = 0
    session.modified = True
    return redirect(url_for("cart"))


@app.route('/helloWorld')
def hello_world() -> str:
    return 'Hello, World!'


@app.route('/twint')
def twint() -> str:
    return render_template("twint.html")


@app.route("/result/<name>")
def result(firstname, surname) -> str:
    app.logger.info(f"Showing result for {firstname}")
    return render_template("erfolg_registriert.html", firstname=firstname, surname=surname)



if __name__ == '__main__':
    app.run(debug=True)  # Debug-Modus aktivieren
