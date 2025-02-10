
from flask import Flask, request, render_template, url_for, redirect, session
from flask_session import Session
import services.math_service as math_service


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


@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    product_name = request.form.get("product_name")
    product_image = request.form.get("product_image")
    product_price = request.form.get("product_price")


    session["cart"] = session.get("cart", []).copy()
    session["cart"].append({"name": product_name, "image": product_image, "price": product_price})
    session.modified = True

    return redirect(url_for("cart"))


@app.route("/clear_cart")
def clear_cart():
    session.pop("cart", None)
    return redirect(url_for("cart"))




@app.route('/helloWorld')
def hello_world() -> str:
    return 'Hello, World!'


@app.route("/submit", methods=["POST"])
def submit():
    app.logger.info("Form submitted")
    name = request.form.get("name")
    return redirect(url_for("result", name=name))


@app.route("/result/<name>")
def result(name) -> str:
    app.logger.info(f"Showing result for {name}")
    return render_template("result.html", name=name)



if __name__ == '__main__':
    app.run(debug=True)  # Debug-Modus aktivieren
