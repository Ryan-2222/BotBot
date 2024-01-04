import discord
from discord.ext import commands

class Administrator(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  # Kick ppl
  @commands.command(name = "kick", pass_context=True)
  @commands.has_permissions(kick_members=True)
  @commands.is_owner()
  async def kick(self, ctx, member:discord.Member, reason=None):
    if ctx.author.guild_permissions.administrator:
        await member.kick(reason=reason)
        embed = discord.Embed(
            description="User" + member.mention + "has been kicked",
            colour=discord.Colour.dark_blue()
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            description="You have no permission!",
            colour=discord.Colour.dark_red()
        )
        await ctx.send(embed=embed)

  # ban ppl
  @commands.command(name = "ban", pass_context=True)
  @commands.has_permissions(kick_members=True)
  @commands.is_owner()
  async def ban(self, ctx, member:discord.Member, reason=None):
      if ctx.author.guild_permissions.administrator:
          await member.ban(reason=reason)
          embed = discord.Embed(
              description="User" + member.mention + "has been banned",
              colour=discord.Colour.dark_blue()
          )
          await ctx.send(embed=embed)
      else:
          embed = discord.Embed(
              description="You have no permission!",
              colour=discord.Colour.dark_red()
          )
          await ctx.send(embed=embed)

  # Give role for users
  @commands.command(pass_context=True)
  async def giverole(self, ctx, user: discord.Member, role: discord.Role):
      if ctx.author.guild_permissions.administrator:
          await user.add_roles(role)
          embed = discord.Embed(description="Successfully added" + role.mention +
                                "from" + user.mention,
                                color=discord.Color.dark_blue())
          await ctx.send(embed=embed)
      else:
          embed = discord.Embed(description="You have no permissions!",
                                color=discord.Color.dark_red())
          await ctx.send(embed=embed)

  # Remove Role for users
  @commands.command(pass_context=True)
  async def rmrole(self, ctx, user: discord.Member, role: discord.Role):
      if ctx.author.guild_permissions.administrator:
          await user.remove_roles(role)
  
          embed = discord.Embed(description="Successfully removed" +
                                role.mention + "from" + user.mention,
                                color=discord.Color.dark_blue())
          await ctx.send(embed=embed)
      else:
          embed = discord.Embed(description="You don't have permissions!",
                                color=discord.Color.dark_red())
          await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(Administrator(bot))