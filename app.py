from flask import Flask, render_template, request, redirect, session, send_file
import sqlite3
import os
from cryptography.fernet import Fernet

app = Flask(__name__)

app.secret_key = "securecloud_secret_key"

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------- ENCRYPTION KEY ----------------

KEY_FILE = "secret.key"


def get_key():

    if not os.path.exists(KEY_FILE):

        key = Fernet.generate_key()

        with open(KEY_FILE, "wb") as file:
            file.write(key)

    else:

        with open(KEY_FILE, "rb") as file:
            key = file.read()

    return key


encryption_key = get_key()

cipher = Fernet(encryption_key)


# ---------------- DATABASE ----------------

def create_database():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            filename TEXT,
            encrypted_filename TEXT
        )
    """)

    conn.commit()

    conn.close()


# ---------------- LOGIN PAGE ----------------

@app.route("/")
def login_page():

    return render_template("login.html")


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")

        cursor = conn.cursor()

        try:

            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, password)
            )

            conn.commit()

            conn.close()

            return redirect("/")

        except sqlite3.IntegrityError:

            conn.close()

            return "Email already registered!"

    return render_template("register.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["POST"])
def login():

    email = request.form["email"]
    password = request.form["password"]

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:

        session["user_id"] = user[0]
        session["name"] = user[1]

        return redirect("/dashboard")

    return "Invalid email or password!"


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        return redirect("/")

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT filename FROM files WHERE user_id=?",
        (session["user_id"],)
    )

    files = cursor.fetchall()

    conn.close()

    file_names = [file[0] for file in files]

    return render_template(
        "dashboard.html",
        name=session["name"],
        files=file_names
    )


# ---------------- UPLOAD ----------------

@app.route("/upload", methods=["POST"])
def upload():

    if "user_id" not in session:

        return redirect("/")

    file = request.files["file"]

    if file.filename == "":
        return "No file selected!"

    original_filename = file.filename

    file_data = file.read()

    encrypted_data = cipher.encrypt(file_data)

    encrypted_filename = original_filename + ".encrypted"

    encrypted_path = os.path.join(
        UPLOAD_FOLDER,
        encrypted_filename
    )

    with open(encrypted_path, "wb") as encrypted_file:

        encrypted_file.write(encrypted_data)

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO files
        (user_id, filename, encrypted_filename)
        VALUES (?, ?, ?)
        """,
        (
            session["user_id"],
            original_filename,
            encrypted_filename
        )
    )

    conn.commit()

    conn.close()

    return redirect("/dashboard")


# ---------------- DOWNLOAD ----------------

@app.route("/download/<filename>")
def download(filename):

    if "user_id" not in session:

        return redirect("/")

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT encrypted_filename
        FROM files
        WHERE filename=? AND user_id=?
        """,
        (filename, session["user_id"])
    )

    result = cursor.fetchone()

    conn.close()

    if not result:

        return "File not found!"

    encrypted_filename = result[0]

    encrypted_path = os.path.join(
        UPLOAD_FOLDER,
        encrypted_filename
    )

    with open(encrypted_path, "rb") as encrypted_file:

        encrypted_data = encrypted_file.read()

    decrypted_data = cipher.decrypt(encrypted_data)

    temp_path = os.path.join(
        UPLOAD_FOLDER,
        "temp_" + filename
    )

    with open(temp_path, "wb") as temp_file:

        temp_file.write(decrypted_data)

    return send_file(
        temp_path,
        as_attachment=True,
        download_name=filename
    )


# ---------------- DELETE ----------------

@app.route("/delete/<filename>")
def delete(filename):

    if "user_id" not in session:

        return redirect("/")

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT encrypted_filename
        FROM files
        WHERE filename=? AND user_id=?
        """,
        (filename, session["user_id"])
    )

    result = cursor.fetchone()

    if result:

        encrypted_filename = result[0]

        encrypted_path = os.path.join(
            UPLOAD_FOLDER,
            encrypted_filename
        )

        if os.path.exists(encrypted_path):

            os.remove(encrypted_path)

        cursor.execute(
            """
            DELETE FROM files
            WHERE filename=? AND user_id=?
            """,
            (filename, session["user_id"])
        )

        conn.commit()

    conn.close()

    return redirect("/dashboard")


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ---------------- START ----------------

if __name__ == "__main__":

    create_database()

    app.run(debug=True)