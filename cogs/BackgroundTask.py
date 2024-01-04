import discord
from discord.ext import commands
import os

class BackgroundTask(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_member_join(self, ctx):
    # Auto Member/Bot Role
    if not ctx.bot:
      autorolemem = discord.utils.get(ctx.guild.roles, name='member')
      await ctx.add_roles(autorolemem)
    else:
      autorolebot = discord.utils.get(ctx.guild.roles, name="I'm not robot")
      await ctx.add_roles(autorolebot)
      
    # Joined Mention
    channel = self.bot.get_channel(int(os.getenv("WEL_CHANNEL")))
    await channel.send(f'{ctx.mention} joined!')

  # User Leave Mention
  @commands.Cog.listener()
  async def on_member_remove(self, ctx):
    channel = self.bot.get_channel(int(os.getenv("LEAVE_CHANNEL")))
    await channel.send(f'{ctx.mention} leaved!')

"""
  # Why hosay so handsome
  @commands.Cog.listener()
  async def on_message(self, message):
    await message.add_reaction("<:seal:762999800227561493>")
"""
  
def setup(bot):
  bot.add_cog(BackgroundTask(bot))