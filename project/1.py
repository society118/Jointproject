from flask import Flask, render_template, redirect, request, session
import bcrypt
from db import get_db_connection,init_db

app = Flask(__name__)
app.secret_key = "hellofriend"

@app.get("/")
def index():
    return render_template(
        "index.html",
        name=session.get("user")
    )
@app.get("/base/")
def base():
    return render_template("base.html",name=session.get("user"))
@app.get("/Linux/")
def linux():
    return render_template("Linux.html", name=session.get("user"))

@app.get("/Windows/")
def windows():
    return render_template("Windows.html", name=session.get("user"))

@app.get("/TempleOS/")
def TempleOS():
    return render_template("TempleOS.html",name=session.get("user"))

@app.get("/autors/")
def avtor():
    return render_template("avtor.html",name=session.get("user"))

@app.get("/register/")
def register_form():
    return render_template("register.html", name=session.get("user"))

@app.post("/register/submit/")
def register_submit():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return "Заполните поля"

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return "Такой пользователь уже существует!"

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hashed_password)
    )
    conn.commit()
    conn.close()

    session["user"] = username
    return redirect("/")

@app.get("/login/")
def login_form():
    return render_template("login.html", name=session.get("user"))

@app.post("/login/submit/")
def login_submit():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return "Введите логин и пароль"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode(), user["password"]):
        session["user"] = username
        return redirect("/")
    else:
        return "Неверный логин или пароль"

@app.get("/logout/")
def logout():
    if "user" in session:
        session.pop("user")
    return redirect("/")

if __name__ == "__main__":
    app.run(port=5052, debug=True)
