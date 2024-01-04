import discord
from discord.ext import commands
import json
from datetime import datetime
import os

class ActiveMemberCheck(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    while True:
      guild = self.bot.get_guild(int(os.getenv("SERVER_ID")))
      if guild == None:
          guild = await self.bot.fetch_guild(int(os.getenv("SERVER_ID")))
  
      with open("lvl_data/active.json", "r") as f:
          active = json.load(f)
  
      role = discord.utils.get(guild.roles, name="Active Member")
      for users, msgdate in active.items():
        date = datetime.utcnow() - datetime.strptime(msgdate.strip(), '%Y-%m-%d %H:%M:%S')
        user = guild.get_member(int(users))
  
        if (date.days < 7):
          await user.add_roles(role)
        else:
          await user.remove_roles(role)
        if 

  @commands.Cog.listener()
  async def on_message(self, ctx):
    if not ctx.author.bot:
      with open("lvl_data/active.json", "r") as f:
        active = json.load(f)

      active[str(ctx.author.id)] = ctx.created_at.strftime('%Y-%m-%d %H:%M:%S')

      with open("lvl_data/active.json", "w") as f:
        json.dump(active, f)

        
  @commands.Cog.listener()
  async def on_voice_state_update(self, ctx, before, after):
    if not ctx.bot:
      with open("lvl_data/active.json", "r") as f:
        active = json.load(f)

      active[str(ctx.id)] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

      with open("lvl_data/active.json", "w") as f:
        json.dump(active, f)

def setup(bot):
  bot.add_cog(ActiveMemberCheck(bot))