from flask import Flask, render_template, url_for, session, redirect, request, jsonify
from threading import Thread
from WebServer.Oauch import Oauch

NAME_KEY = "name"

app = Flask(__name__)
app.secret_key = "Yowhatsupguysiamryan"

# Real Bot's State of Connection 
@app.route("/conn_state")
def conn_state():
  return "Nyan Cat is now online!"

@app.route('/login')
def login():
  return render_template("login.html", discord_url=Oauch.DISCORD_LOGIN_URL)

@app.route('/OAuth2/discord')
def oauth():
  access_token = Oauch.get_token(request.args.get('code'))
  session['ACCESS_TOKEN'] = access_token
  return redirect('/dashboard')

@app.route('/')
@app.route('/dashboard')
def dashboard():
  if 'ACCESS_TOKEN' not in session:
    return redirect(url_for('login'))
  user_guilds = Oauch.get_user_guilds(session.get('ACCESS_TOKEN'))
  bot_guilds = Oauch.get_bot_guilds()
  mutual_guilds = Oauch.get_intersect_guilds(user_guilds, bot_guilds)
  return render_template('dashboard.html', guilds=mutual_guilds)
 
@app.route('/logout')
def logout():
    session.clear()
    return redirect("/login")

@app.route("/guild/<guild_id>")
def guild(guild_id: int):
  if 'ACCESS_TOKEN' not in session:
    return redirect(url_for('login'))
  guild_info = Oauch.get_guild_data(guild_id)
  return render_template('guild.html', guild=guild_info)

@app.route("/guild/<guild_id>/")
def backup():
  if 'ACCESS_TOKEN' not in session:
    return redirect(url_for('login'))

def run():
  app.run(host="0.0.0.0", port="5050")


def server():
  server = Thread(target=run)
  server.start()
