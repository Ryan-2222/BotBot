from flask import Flask, render_template, url_for, session, redirect, request, jsonify
from threading import Thread

NAME_KEY = "name"

app = Flask(__name__)
app.secret_key = "Yowhatsupguysiamryan"

@app.route('/')
@app.route('/home')
def home():
  if NAME_KEY not in session:
    return redirect(url_for("login"))
  return render_template("index.html", **{"login": True, "session": session})


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session[NAME_KEY] = request.form["username"]
            return redirect(url_for('home'))
    return render_template("login.html", **{"session": session})


@app.route("/logout")
def logout():
    session.pop(NAME_KEY, None)
    return redirect(url_for("login"))

# Real Bot's State of Connection 
@app.route("/conn_state")
def conn_state():
  return "Nyan Dog is now online!"

@app.route("/<usr>")
def user(usr):
  return f"Hello! {usr}"

def run():
  app.run(host="0.0.0.0", port="5050")


def keep_alive():
  server = Thread(target=run)
  server.start()
