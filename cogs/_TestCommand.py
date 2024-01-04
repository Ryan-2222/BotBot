import discord
from discord.ext import commands
import os


class CommandTest(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_message(self, ctx):
    print(ctx.author.id)
    if ctx.author.id == 600958759350566913:
      await ctx.delete()

def setup(bot):
  bot.add_cog(CommandTest(bot))