import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .models import Product, Order, OrderItem
from . import db
bp = Blueprint("checkout", __name__)

STRIPE_SECRET = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE = os.environ.get("STRIPE_PUBLISHABLE_KEY")

@bp.app_context_processor
def inject_keys():
    return {"STRIPE_PUBLISHABLE_KEY": STRIPE_PUBLISHABLE}

def _cart_lines():
    cart = session.get("cart", {})
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
    return lines, total_cents

@bp.route("/", methods=["GET"])
def checkout_page():
    lines, total_cents = _cart_lines()
    return render_template("checkout.html", lines=lines, total_cents=total_cents, stripe_enabled=bool(STRIPE_SECRET))

@bp.route("/pay", methods=["POST"])
def create_checkout():
    # If Stripe keys are present, redirect to Stripe Checkout; else mock success
    lines, total_cents = _cart_lines()
    email = request.form.get("email", "")
    if not lines:
        flash("Your cart is empty.", "error")
        return redirect(url_for("main.index"))
    if STRIPE_SECRET:
        import stripe
        stripe.api_key = STRIPE_SECRET
        success_url = url_for("checkout.success", _external=True) + "?session_id={CHECKOUT_SESSION_ID}"
        cancel_url = url_for("main.cart_view", _external=True)
        session_obj = stripe.checkout.Session.create(
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
            customer_email=email or None,
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": l["product"].name},
                    "unit_amount": l["product"].price_cents
                },
                "quantity": l["qty"]
            } for l in lines]
        )
        return redirect(session_obj.url)
    else:
        # Mock order without Stripe for demo
        order = Order(user_email=email or None, total_cents=total_cents, stripe_session_id=None)
        db.session.add(order)
        db.session.flush()
        for l in lines:
            db.session.add(OrderItem(order_id=order.id, product_id=l["product"].id, quantity=l["qty"], unit_price_cents=l["product"].price_cents))
        db.session.commit()
        session["cart"] = {}
        return redirect(url_for("checkout.success"))

@bp.route("/success")
def success():
    # In real app, you'd verify the Stripe session and mark the order paid
    return render_template("success.html")
