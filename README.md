# Flask E-Commerce Demo (Fixed for Render)

Minimal demonstration e-commerce store built with Flask.

## Deploy to Render
1. Push this folder to GitHub.
2. In Render: New → Web Service → Build from repository.
3. Render will detect `render.yaml` and deploy.
4. Visit the live URL to see your store.

## Local run
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```
