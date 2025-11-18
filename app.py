# app.py - FULLY UPGRADED: Sign up + Login + Per-user private folders + DATE FILTER FIXED!
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, session, abort
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = "super-secret-key-change-in-production-2025"

UPLOAD_ROOT = "uploads"
os.makedirs(UPLOAD_ROOT, exist_ok=True)

# In-memory users DB (replace with SQLite later if you want)
# Format: username: {password_hash, name}
USERS = {
    "admin": {
        "password": generate_password_hash("admin123"),
        "name": "Admin User"
    }
}

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated

def get_current_user_folder():
    username = session["username"]
    folder = os.path.join(UPLOAD_ROOT, username)
    os.makedirs(folder, exist_ok=True)
    return folder

# ==================== CUSTOM JINJA FILTER FOR DATES (THIS WAS MISSING!) ====================
@app.template_filter("timestamp_to_date")
def timestamp_to_date(ts):
    return datetime.fromtimestamp(ts).strftime("%b %d, %Y at %I:%M %p")
# =========================================================================================

# ==================== ROUTES ====================

@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"].strip().lower()
        name = request.form["name"].strip()
        password = request.form["password"]

        if not username or not password or not name:
            flash("All fields are required!", "danger")
        elif username in USERS:
            flash("Username already taken!", "danger")
        elif len(password) < 6:
            flash("Password must be at least 6 characters!", "danger")
        else:
            USERS[username] = {
                "password": generate_password_hash(password),
                "name": name
            }
            flash("Account created! Please login.", "success")
            return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form["username"].strip().lower()
        password = request.form["password"]

        user = USERS.get(username)
        if user and check_password_hash(user["password"], password):
            session["username"] = username
            session["name"] = user["name"]
            flash(f"Welcome back, {user['name']}!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("dashboard"))
        else:
            flash("Invalid username or password!", "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    folder = get_current_user_folder()
    files = []
    for f in os.listdir(folder):
        fp = os.path.join(folder, f)
        if os.path.isfile(fp):
            stat = os.stat(fp)
            files.append({
                "name": f,
                "size": stat.st_size,
                "mtime": stat.st_mtime
            })
    files.sort(key=lambda x: x["mtime"], reverse=True)

    return render_template("dashboard.html", files=files, name=session["name"])

@app.route("/upload", methods=["POST"])
@login_required
def upload():
    if "file" not in request.files:
        flash("No file selected", "danger")
        return redirect(url_for("dashboard"))

    file = request.files["file"]
    if file.filename == "":
        flash("No file selected", "danger")
        return redirect(url_for("dashboard"))

    filename = secure_filename(file.filename)
    folder = get_current_user_folder()
    filepath = os.path.join(folder, filename)

    # Avoid overwrite
    if os.path.exists(filepath):
        base, ext = os.path.splitext(filename)
        filename = f"{base}_{int(datetime.now().timestamp())}{ext}"

    file.save(os.path.join(folder, filename))
    flash("File uploaded successfully!", "success")
    return redirect(url_for("dashboard"))

@app.route("/download/<filename>")
@login_required
def download(filename):
    folder = get_current_user_folder()
    safe_path = os.path.join(folder, filename)
    if not os.path.exists(safe_path):
        abort(404)
    return send_from_directory(folder, filename, as_attachment=True)

@app.route("/delete/<filename>")
@login_required
def delete(filename):
    folder = get_current_user_folder()
    filepath = os.path.join(folder, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        flash("File deleted!", "success")
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)