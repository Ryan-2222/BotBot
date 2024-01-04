# command that won't use (backup)


#kick 
@client.command(name = "kick", pass_context=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, member:discord.Member, reason=None):
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

#ban
@client.command(name = "ban", pass_context=True)
@commands.has_permissions(kick_members=True)
async def ban(ctx, member:discord.Member, reason=None):
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
#exile
@client.command(pass_context=True)
async def exile(ctx, member: discord.Member):
    if ctx.author.guild_permissions.administrator:
        channel = discord.utils.get(ctx.guild.voice_channels, name="西伯利亞")
        await member.move_to(channel)

#sao
@client.command(pass_context=True)
async def sao(ctx, user: discord.Member):
  embed = discord.Embed(
    title="視頻流出",
    description=user.mention + " found that 肥哥哥 is very sao and his video is exposed to everyone!?"
  )
  await ctx.reply(embed=embed)
 