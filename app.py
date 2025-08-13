from flask import Flask, render_template, redirect, url_for, request, flash

app = Flask(__name__)
app.secret_key = "demo_secret_key"

# Mock product data
PRODUCTS = [
    {"id": 1, "name": "Wireless Headphones", "price": 99.99, "description": "Noise-cancelling over-ear headphones."},
    {"id": 2, "name": "Smartwatch", "price": 149.99, "description": "Track your fitness and notifications."},
    {"id": 3, "name": "Gaming Mouse", "price": 49.99, "description": "High precision and customizable buttons."}
]

@app.route("/")
def home():
    return render_template("home.html", products=PRODUCTS)

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        flash("Product not found!", "error")
        return redirect(url_for("home"))
    return render_template("product_detail.html", product=product)

@app.route("/checkout", methods=["POST"])
def checkout():
    product_id = int(request.form.get("product_id"))
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if product:
        flash(f"Successfully purchased {product['name']} for ${product['price']}!", "success")
    else:
        flash("Product not found!", "error")
    return redirect(url_for("home"))
