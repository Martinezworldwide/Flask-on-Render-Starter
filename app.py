import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/")
def index():
    return jsonify({
        "app": "Flask on Render starter",
        "message": "It works! 🎉",
        "docs": "See README.md for deployment steps."
    })

@app.get("/healthz")
def healthz():
    return {"ok": True}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
