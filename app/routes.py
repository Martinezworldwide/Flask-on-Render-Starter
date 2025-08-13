from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .models import Product
from . import db

bp = Blueprint("main", __name__)

def _cart():
    return session.setdefault("cart", {})  # {product_id: qty}

@bp.route("/")
def index():
    q = request.args.get("q")
    query = Product.query
    if q:
        like = f"%{q}%"
        query = query.filter(Product.name.ilike(like) | Product.description.ilike(like))
    products = query.order_by(Product.created_at.desc()).all()
    return render_template("index.html", products=products, q=q or "")

@bp.route("/product/<int:pid>")
def product_detail(pid):
    p = Product.query.get_or_404(pid)
    return render_template("product_detail.html", p=p)

@bp.route("/cart")
def cart_view():
    cart = _cart()
    ids = [int(pid) for pid in cart.keys()]
    products = Product.query.filter(Product.id.in_(ids)).all() if ids else []
    lines = []
    total_cents = 0
    for p in products:
        qty = int(cart.get(str(p.id), 0))
        if qty <= 0:
            continue
        line_total = qty * p.price_cents
        total_cents += line_total
        lines.append({"product": p, "qty": qty, "line_total_cents": line_total})
    return render_template("cart.html", lines=lines, total_cents=total_cents)

@bp.route("/cart/add", methods=["POST"])
def cart_add():
    pid = request.form.get("product_id")
    qty = int(request.form.get("qty", 1))
    cart = _cart()
    cart[pid] = cart.get(pid, 0) + qty
    session.modified = True
    flash("Added to cart!", "ok")
    return redirect(request.referrer or url_for("main.cart_view"))

@bp.route("/cart/update", methods=["POST"])
def cart_update():
    pid = request.form.get("product_id")
    qty = max(0, int(request.form.get("qty", 0)))
    cart = _cart()
    if qty == 0:
        cart.pop(pid, None)
    else:
        cart[pid] = qty
    session.modified = True
    return redirect(url_for("main.cart_view"))

@bp.route("/cart/clear", methods=["POST"])
def cart_clear():
    session["cart"] = {}
    session.modified = True
    return redirect(url_for("main.cart_view"))

# Simple admin: add products (no auth gate for demo; protect in production)
@bp.route("/admin/products", methods=["GET", "POST"])
def admin_products():
    if request.method == "POST":
        name = request.form.get("name", "")
        sku = request.form.get("sku", "")
        price_cents = int(float(request.form.get("price", "0")) * 100)
        description = request.form.get("description", "") or ""
        image_url = request.form.get("image_url", "") or ""
        db.session.add(Product(name=name, sku=sku, price_cents=price_cents, description=description, image_url=image_url))
        db.session.commit()
        return redirect(url_for("main.admin_products"))
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template("admin_products.html", products=products)
