# Flask Shop (Render-ready)

A minimal, real e‑commerce demo:
- Product catalog (searchable)
- Session cart (server-side)
- Checkout page
- Optional Stripe Checkout integration
- Simple admin to add products

## Deploy on Render (via GitHub)
1. Push this folder to a new GitHub repo.
2. In Render: **New → Web Service → Build & deploy from a Git repository**.
3. Pick your repo; Render will use `render.yaml`. Click **Create Web Service**.
4. (Optional) Add a **PostgreSQL** instance in Render. `DATABASE_URL` will be injected automatically.
5. (Optional) Add `STRIPE_PUBLISHABLE_KEY` and `STRIPE_SECRET_KEY` env vars for live Stripe Checkout.

## Local run
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=wsgi.py
flask run --debug
```

## Seed some products
Visit `/admin/products` to add items quickly (demo only; protect in production).

## Routes
- `/` — product list & search
- `/product/<id>` — details
- `/cart` — view/update/clear cart
- `/checkout` — checkout page; posts to `/checkout/pay`
- `/checkout/success` — success page
- `/auth/login`, `/auth/register` — basic auth
- `/admin/products` — add/list products (no auth gate in demo)
