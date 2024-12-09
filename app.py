from flask import Flask, session, redirect, request, render_template, flash
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.secret_key = "9834dh095ohqdlksajdfc9234!5"
admin_username = os.getenv('admin_username')
admin_password = os.getenv('admin_password')


@app.route('/')
def index():  # put application's code here
    return redirect("/dashboard")


@app.route("/dashboard")
def dashboard():
    if not session.get('logged_in'):
        return redirect("/login")
    return "Welcome to admin dashboard!"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == admin_username and password == admin_password:
            session["logged_in"] = True
            return redirect('/dashboard')
        else:
            flash("Invalid credentials. Try again.")
    return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop("logged_in", None)
    return redirect("/login")


if __name__ == '__main__':
    app.run()
