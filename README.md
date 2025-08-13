# Flask E-Commerce Demo

A minimal demonstration of an e-commerce store built with Flask, ready to deploy on Render.

## Features
- Home page showing products
- Product detail pages
- Mock checkout with flash messages

## Deployment on Render via GitHub
1. Push this project to a new GitHub repository.
2. In Render: New → Web Service → Build from Git repository.
3. Render will detect `render.yaml` and build automatically.
4. Visit your Render URL to see the store.

## Local Development
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```
