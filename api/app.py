from flask import Flask, request
import sqlite3
import subprocess
import hashlib
import os

app = Flask(__name__)


SECRET_KEY = "dev-secret-key-12345"   # Hardcoded secret


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)

    result = cursor.fetchone()
    if result:
        return {"status": "success", "user": username}

    return {"status": "error", "message": "Invalid credentials"}


@app.route("/ping", methods=["POST"])
def ping():
    host = request.json.get("host", "")

    # Command Injection : shell=True
    cmd = f"ping -c 1 {host}"
    output = subprocess.check_output(cmd, shell=True)

    return {"output": output.decode()}


# -------------------------------------------------------------------------
@app.route("/compute", methods=["POST"])
def compute():
    expression = request.json.get("expression", "1+1")

    # Vulnérabilité majeure : exécution de code utilisateur
    result = eval(expression)   # CRITIQUE

    return {"result": result}


# -------------------------------------------------------------------------
# Vulnérabilité 5 : Hash MD5 (Bandit B303 Weak Cryptography)
# -------------------------------------------------------------------------
@app.route("/hash", methods=["POST"])
def hash_password():
    pwd = request.json.get("password", "admin")

    # MD5 = weak cryptography
    hashed = hashlib.md5(pwd.encode()).hexdigest()

    return {"md5": hashed}


# -------------------------------------------------------------------------
# Vulnérabilité 6 : Ouverture de fichier sans contrôle (Bandit B322/B325)
# -------------------------------------------------------------------------
@app.route("/readfile", methods=["POST"])
def readfile():
    filename = request.json.get("filename", "test.txt")

    # Vulnérabilité : path traversal possible (“../../etc/passwd”)
    with open(filename, "r") as f:
        content = f.read()

    return {"content": content}


# -------------------------------------------------------------------------
# Vulnérabilité 7 : Exposition d'informations sensibles
# -------------------------------------------------------------------------
@app.route("/debug", methods=["GET"])
def debug():
    # Renvoie des détails sensibles -> mauvaise pratique
    return {
        "debug": True,
        "secret_key": SECRET_KEY,
        "environment": dict(os.environ)
    }


# -------------------------------------------------------------------------
# Endpoint safe pour test
# -------------------------------------------------------------------------
@app.route("/hello", methods=["GET"])
def hello():
    return {"message": "Welcome to the DevSecOps vulnerable API"}


# -------------------------------------------------------------------------
# App
# -------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
