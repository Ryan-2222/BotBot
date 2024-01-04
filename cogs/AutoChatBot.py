import discord
from discord.ext import commands
import os
import requests


class AutoChatBot(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_message(self, message):
    if self.bot.user == message.author:
      return
    elif "<@803138272398278677>" in message.content or message.channel.id == message.author.dm_channel.id:
      try:
        url = "https://random-stuff-api.p.rapidapi.com/ai"
        text = message.content.replace("<@803138272398278677>", "")
        
        querystring = {"msg":text, "bot_name":"Nyan Cat","bot_gender":"male","bot_age":"Unlimited","bot_company":"Nyan Cat","bot_location":"HK","bot_build":"2011","bot_birth_year":"2011","bot_birth_date":"2nd April, 2011","bot_birth_place":"YouTube","bot_favorite_color":"Blue"}
        
        headers = {
        	"Authorization": os.getenv("API_KEY_AI_CHAT"),
        	"X-RapidAPI-Key": "62f2a1b6acmshd769a5597d0fa92p162b8djsn6ec4f14fbd2d",
        	"X-RapidAPI-Host": "random-stuff-api.p.rapidapi.com"
        }
        
        response = requests.request("GET", url, headers=headers, params=querystring, timeout=3)
        
        await message.reply(response.json()["AIResponse"])
      except Exception as e:
        await message.channel.send(e)
        return

def setup(bot):
  bot.add_cog(AutoChatBot(bot))
  