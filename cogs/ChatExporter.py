import discord
from discord.ext import commands
import chat_exporter
import io

class ChatExporter(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def save(self, ctx: commands.Context):
      await chat_exporter.quick_export(ctx.channel)


def setup(bot):
  bot.add_cog(ChatExporter(bot))