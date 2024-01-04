import discord
from discord.ext import commands
from datetime import datetime
import pytz
import os

r18_channel = [942803863730278501,  942153544260259933, 723185702677774449, 1010995530375102586]

block_channel = [798421273263996928, 722848989489397901, 709442743914725497, 996002622618218636, 996002622618218636, 907992373378822174, 1068554814516113438]

class Logger(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_message(self, ctx):
    if ctx.channel.id in block_channel:
      return
    else:
      if ctx.channel.id in r18_channel:
        channel = discord.utils.get(ctx.guild.channels, name='r18-logger')
      else:
        channel = discord.utils.get(ctx.guild.channels, name='logger')
      if ctx.author == self.bot.user: 
        return
      else:
          list = [".clear", "<", "?"]
          if not any([x in ctx.content for x in list]):
            embed = discord.Embed(
              title = "Message sent", description = ctx.author.mention, 
              color = ctx.author.color,
              timestamp = datetime.now(pytz.timezone("Asia/Hong_Kong"))
            )
            if len(ctx.attachments) > 0:
              embed.add_field(name = "URL: ", value = ctx.attachments[0].url)
            embed.add_field(name = "Message: ", value=ctx.content if ctx.content else "None")
            embed.add_field(name = "Channel: ", value = ctx.channel.mention)
            await channel.send(embed=embed)
   
  @commands.Cog.listener()
  async def on_message_edit(self, before, after):
    if before.channel.id in r18_channel:
      channel = discord.utils.get(before.guild.channels, name='r18-logger')
    else:
      channel = discord.utils.get(before.guild.channels, name='logger')
    if self.bot.user == before.author:
      pass
    else:
      embed = discord.Embed(
        title = "Message edited",
        description = before.author.mention, color = before.author.color,
        timestamp = datetime.now(pytz.timezone("Asia/Hong_Kong"))
      )
      embed.add_field(name = "Channel: ", value = before.channel.mention)
      embed.add_field(name = "Before: ", value = before.content)
      embed.add_field(name = "After: ", value = after.content)
      await channel.send(embed=embed)
   
def setup(bot):
  bot.add_cog(Logger(bot))