from flask import Flask, request
import sqlite3
import subprocess

app = Flask(__name__)

# -------------------------------------------------------------------------
# Vulnérabilité 1 : Secret codé en dur (CodeQL le détecte)
# -------------------------------------------------------------------------
SECRET_KEY = "12345"


# -------------------------------------------------------------------------
# Vulnérabilité 2 : SQL Injection
# -------------------------------------------------------------------------
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Vulnérabilité volontaire : SQL Injection via f-string
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)

    result = cursor.fetchone()
    if result:
        return {"status": "success", "user": username}

    return {"status": "error", "message": "Invalid credentials"}


# -------------------------------------------------------------------------
# Vulnérabilité 3 : Command Injection (CodeQL + Bandit la détectent)
# -------------------------------------------------------------------------
@app.route("/ping", methods=["POST"])
def ping():
    host = request.json.get("host", "")

    # Vulnérabilité : shell=True + input utilisateur → CRITIQUE
    cmd = f"ping -c 1 {host}"
    output = subprocess.check_output(cmd, shell=True)

    return {"output": output.decode()}


# -------------------------------------------------------------------------
# Vulnérabilité 4 : Endpoint debug exposé
# -------------------------------------------------------------------------
@app.route("/debug", methods=["GET"])
def debug():
    # Endpoint qui expose des clés → Mauvaise pratique
    return {
        "debug": True,
        "secret_key": SECRET_KEY,
        "message": "Debug mode active"
    }


# -------------------------------------------------------------------------
# Endpoint simple : non vulnérable (pour test normal)
# -------------------------------------------------------------------------
@app.route("/hello", methods=["GET"])
def hello():
    return {"message": "Welcome to the DevSecOps vulnerable API"}


# -------------------------------------------------------------------------
# Lancement application
# -------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
