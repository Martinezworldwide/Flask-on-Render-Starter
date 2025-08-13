# Flask on Render — Starter

Minimal Flask app ready to deploy on **Render** via GitHub.

## Quick start (GitHub → Render)

1. **Create a GitHub repo** and push this folder's contents:
   ```bash
   git init
   git add .
   git commit -m "Flask on Render starter"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo>.git
   git push -u origin main
   ```
2. **On Render**: click **New → Web Service**, choose **Build & deploy from a Git repository**, and connect your GitHub.
3. Pick your repo, keep the default settings (the app uses `render.yaml`), and click **Create Web Service**.
4. After build finishes, visit the URL Render gives you. You should see JSON from `/` and `{"ok": true}` at `/healthz`.

### What’s included
- `app.py` — tiny Flask app with `/` and `/healthz`
- `requirements.txt` — only Flask + Gunicorn
- `render.yaml` — defines a web service using Gunicorn threads

### Scaling notes
- Gunicorn starts with `WEB_CONCURRENCY=2` (threads worker). Increase this in Render → **Environment** if needed.
- Keep the app stateless for easy horizontal scaling. Persist data in managed services (e.g., Render PostgreSQL, Redis, S3-compatible storage).

### Add PostgreSQL later (optional)
1. Create a **PostgreSQL** instance in Render and copy `DATABASE_URL`.
2. Add it as an environment variable in your web service.
3. Install DB dependencies in `requirements.txt` (e.g., `SQLAlchemy`, `psycopg2-binary`) and use it in your app code.

### Local run
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
# or
gunicorn -w 2 -k gthread -b 0.0.0.0:5000 app:app
```

---
If you want a version with a sample Postgres model, Redis caching, and a worker service, let me know and I’ll add those files.
