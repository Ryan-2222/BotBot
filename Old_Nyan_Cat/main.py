import discord
import json
import requests
import os

from keep_alive import keep_alive
from discord.ext import commands, tasks
from random import choice
from typing import Optional
from mcstatus import MinecraftServer

with open("data/config.json", "r") as f:
    config = json.load(f)
    status_text = config['status_text']
    wel_channel = config['welcome_channel']
    leave_channel = config['exit_channel']

intent = discord.Intents.all()
client = commands.Bot(command_prefix=".", intents=intent)


@client.event
async def on_ready():
    print(">>Bot is online!<<")
    await update_status.start()


@client.event
# AutoRole
async def on_member_join(ctx):
    autorolemem = discord.utils.get(ctx.guild.roles, name='member')
    await ctx.add_roles(autorolemem)
    # Joined Mention
    channel = client.get_channel(wel_channel)
    await channel.send(f'{ctx.mention} joined!')


async def on_member_join(member):
    # Level System
    with open('data/users.json', 'r') as f:
        users = json.load(f)
    await update_data(users, member)
    with open('data/users.json', 'w') as f:
        json.dump(users, f)


# member leave mention
@client.event
async def on_member_remove(ctx):
    channel = client.get_channel(leave_channel)
    await channel.send(f'{ctx.mention} leaved!')


# Level Up System Background-Processing
# Level System Detect Messages
@client.event
async def on_message(message):
    if message.author.bot == False:
        with open('data/users.json', 'r') as f:
            users = json.load(f)
        await update_data(users, message.author)
        await add_experience(users, message.author, 5)
        await level_up(users, message.author, message)
        with open('data/users.json', 'w') as f:
            json.dump(users, f)
    await client.process_commands(message)


# Level Up System update data
async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1


# Level System Add experience
async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp


# Level System Level Up
async def level_up(users, user, message):
    with open('data/levels.json', 'r') as g:
        levels = json.load(g)
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience**(1 / 4))
    if lvl_start < lvl_end:
        # print(user)
        # print(user.id)
        # print(users)
        # await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}')
        users[f'{user.id}']['level'] = lvl_end


# Level System Background End


@client.command()
async def level(ctx, member: discord.Member = None):
    if not member:
        id = ctx.message.author.id
        with open('data/users.json', 'r') as f:
            users = json.load(f)
        lvl = str(users[str(id)]['level'])
        exp = str(users[str(id)]['experience'])

        name = ctx.message.author
        url = name.avatar_url

        embed = discord.Embed(title="Level info",
                              description="Level:" + " " + lvl +
                              "\nExperience" + " " + exp,
                              color=discord.Color.dark_blue())
        embed.set_thumbnail(url=url)

        await ctx.send(name.mention + " " + f'is now level {lvl}!')
        #print(ctx.message.author.name)
        await ctx.send(embed=embed)
    else:
        id = member.id
        with open('data/users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        await ctx.send(f'{member} is at level {lvl}!')


# Level System End


@tasks.loop(seconds=10)
async def update_status():
    await client.change_presence(activity=discord.Game(choice(status_text)))


@client.command()
async def clear(ctx, amount: Optional[int] = 1, showtext=None):
    await ctx.channel.purge(limit=amount + 1)
    if showtext is None:
        await ctx.send(f'*Delete {amount} message(s)*')
    elif showtext == "None" or "none":
        pass
    else:
        await ctx.send(f'*Delete {amount} message(s)*')


@client.command(pass_context=True)
async def giverole(ctx, user: discord.Member, role: discord.Role):
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


@client.command(pass_context=True)
async def rmrole(ctx, user: discord.Member, role: discord.Role):
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


@client.command(aliases=["隻抽"])
async def fight(ctx, user: discord.Member):
    embed = discord.Embed(title="隻抽 challenge",
                          description=user.mention + " " + ctx.author.mention +
                          " wants 隻抽 with you!")
    await ctx.reply(embed=embed)
    # await ctx.message.delete()


#exile
@client.command(pass_context=True)
async def exile(ctx, user: discord.Member):
    channel = discord.utils.get(ctx.guild.voice_channels, name="西伯利亞")
    # print(channel)
    await user.move_to(channel)
    embed = discord.Embed(description=user.mention + " has been exiled",
                          color=discord.Color.dark_blue())
    await ctx.send(embed=embed)


@client.command(name="mc", pass_context=True)
async def mc(ctx, ip, ip2: Optional[int] = 25565):
    try:
        ip3 = str(ip2)
        server = MinecraftServer.lookup(ip + ":" + ip3)
        status = server.status()

        embed = discord.Embed(
            title="Server Info:",
            description="Server IP:" + ip + "\nPort: " + ip3 + "\n" +
            "\nPlayer Online: {0} \nLatency: {1}".format(
                status.players.online, status.latency) + "ms",
            color=discord.Color.dark_blue())
        embed.set_thumbnail(
            url=
            "https://i1.wp.com/www.craftycreations.net/wp-content/uploads/2019/08/Grass-Block-e1566147655539.png?fit=500%2C500&ssl=1"
        )
        await ctx.send(embed=embed)
    except BrokenPipeError:
        embed = discord.Embed(
            description=
            "Server Port is wrong! Please check the wrong port and try again!")
        await ctx.send(embed=embed)
    except:
        embed = discord.Embed(
            description="Server IP is wrong! Please try again!")
        await ctx.send(embed=embed)


keep_alive()

client.run(os.getenv("TOKEN"))
