from flask import Flask, render_template, g, flash, request
from flask.ext.login import login_user, logout_user, current_user, login_required, LoginManager
from db_connector import User, Character, Stat, StatType, Achievement
import os

app = Flask(__name__, template_folder="/home/ubuntu/dnd_site/static")
app.secret_key = "abc123"

login_manager = LoginManager()
login_manager.init_app(app)

@app.before_request
def before_request():
    g.user = current_user

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/", methods=["GET"])
def main():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
   return ""



if __name__ == "__main__":
    app.run("0.0.0.0", port=80)
