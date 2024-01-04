import discord
from discord.ext import commands
import os
from WebServer import app

intents = discord.Intents.all()
client = commands.Bot(command_prefix=">", intents=intents)

# Cogs Here
extensions = [
    "cogs.BackgroundTask", "cogs.Administrator", "cogs.UsersCommands",
    "cogs.LevelSystem", "cogs.Logger"
]

# Chat_Exporter v1.7.3
# os.system("rsync -av --exclude=~/Nyan-Cat/venv/lib/python3.8/site-packages/chat_exporter* ~/Nyan-Cat/venv/lib/python3.8/site-packages/chat_exporter/ ~/.cache/pip/pool/3a/1f/c1")
# import chat_exporter


@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Game("Nyan Dog and Discord Server"))
    # chat_exporter.init_exporter(client)
    #
    try:
        for guild in client.guilds:
            os.mkdir(f"WebServer/templates/backup/{guild.id}")
    except FileExistsError:
        pass
    print("Bot is now online!")


if __name__ == "__main__":
    for ext in extensions:
        try:
            client.load_extension(ext)
            print(f"Finished loading {ext}")
        except Exception as e:
            print(f"Failed to load {ext} for [EXCEPTION] {e}")

# App Server Start
app.server()

# Client Start
try:
    client.run(os.getenv("TOKEN"))
except:
    os.system("kill 1")
    client.run(os.getenv("TOKEN"))
