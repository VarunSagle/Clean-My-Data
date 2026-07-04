from flask import session, redirect, url_for, render_template, Flask, request, Blueprint
from flask_bcrypt import Bcrypt
import mysql.connector

auth = Blueprint("auth", __name__)
bcrypt = Bcrypt()


def get_connector():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Varun@2003",
        database = "cleanmydata"
    )

@auth.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        hashed = bcrypt.generate_password_hash(password).decode("utf-8")

        conn = get_connector()
        cursor = conn.cursor()

        cursor.execute(""" INSERT INTO users(username, email, password) VALUES (%s, %s, %s) """ , (username, email, hashed))

        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("auth.login"))
    return render_template("register.html")


@auth.route('/login', methods=['GET', 'POST'])
def login():
    error=None
    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_connector()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(" SELECT * FROM users WHERE email = %s ", (email,))

        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and bcrypt.check_password_hash(user['password'], password):
            session["user"] = user["username"]
            return redirect(url_for('fill_data'))

        else:
            return "Invalid Login"
    return render_template("login.html", error=error)


@auth.route('/logout')
def logout():
    
    session.clear()
    return redirect(url_for("auth.login"))


# if __name__ == "__main__":
#     app.run(debug=True)
