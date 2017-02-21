from flask import Flask, render_template, g, flash, request, redirect
from flask.ext.login import login_user, logout_user, current_user, login_required, LoginManager
from db_connector import User, Character, Stat, StatType, Achievement, get_user_by_username, get_user_by_id
import os

app = Flask(__name__, template_folder="/home/ubuntu/dnd_site/static")
app.secret_key = "abc123"

login_manager = LoginManager()
login_manager.init_app(app)

@app.before_request
def before_request():
    g.user = current_user

@login_manager.request_loader
def load_user(request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')
    if token is not None:
        username,password = token.split(":") # naive token
        user_entry = User.get(username)
        if (user_entry is not None):
            user = User(user_entry[0],user_entry[1])
            if (user.password == password):
                return user
            return None

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

@app.route("/", methods=["GET"])
def main():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    try:
        user = get_user_by_username(request.form.get("username"))
        if request.form.get("password") == user.password:
            login_user(user)
            return redirect('/characters')
        else:
            return "Bad username or password"
    except Exception as e:
        return "No user: {}".format(str(e))
    return "Fail!"

@app.route("/characters", methods=["GET"])
@login_required
def get_characters():
    chars = Character.get_all()
    return render_template("characters.html", characters=chars)

@app.route("/characters/<int:id>", methods=["GET"])
@login_required
def get_character(id):
    char = Character.get_by_id(id)
    character_stats = get_stats(id)
    all_stats = get_stats_types()
    for stat in character_stats:
        for s in all_stats:
            if stat.stat_id == s.id:
                stat.name = s.name
    return render_template("stats.html", character=char, stats=character_stats)

@app.route("/characters", methods=["POST"])
@login_required
def post_character():
    new_char_name = request.form.get("char_name")
    char = Character(name=new_char_name)
    char.commit()
    return redirect("/characters")

@app.route("/stats/<int:character_id>", methods=["GET"])
@login_required
def get_stats(character_id):
    stat_types = get_stats_types()
    char_stats = Stat.get_by_character(character_id)
    char_stat_ids = set([s.stat_id for s in char_stats])
    for s in stat_types:
        if s.id not in char_stat_ids:
            stat = Stat(character_id=character_id, stat_id=s.id, value=0)
            stat.commit()
    char_stats = Stat.get_by_character(character_id)
    return char_stats

@app.route("/stats/types", methods=["GET"])
@login_required
def get_stats_types():
    return StatType.get_all()

@app.route("/characters/<int:character_id>/save", methods=["POST"])
@login_required
def post_character_stats(character_id):
    stats = Stat.get_by_character(character_id)
    for s in stats:
        new_stat = request.form.get(str(s.id))
        s.value = int(new_stat)
        s.commit()
    return redirect("/characters/{}".format(character_id))

@app.route("/stats/types", methods=["POST"])
@login_required
def post_stats_type():
    stat_name = request.form.get("stat_name")
    if stat_name == "":
        return redirect(request.referrer)
    stat = StatType(name=stat_name)
    stat.commit()
    return redirect(request.referrer)

if __name__ == "__main__":
    app.run("0.0.0.0", port=80)
