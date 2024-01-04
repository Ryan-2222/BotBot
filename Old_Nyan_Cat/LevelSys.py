import discord
import json
import os

from discord.ext import commands, tasks

client = commands.Bot(command_prefix=".")

def Level_Up():
    @client.event
    async def on_ready():
        print("Bot is now online!")

    @client.event
    async def on_member_join(member):
        with open('data/users.json', 'r') as f:
            users = json.load(f)

        await update_data(users, member)

        with open('data/users.json', 'w') as f:
            json.dump(users, f)


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


    async def update_data(users, user):
        if not f'{user.id}' in users:
            users[f'{user.id}'] = {}
            users[f'{user.id}']['experience']  = 0
            users[f'{user.id}']['level'] = 1


    async def add_experience(users, user, exp):
        users[f'{user.id}']['experience'] += exp


    async def level_up(users, user, message):
        with open('data/levels.json', 'r') as g:
            levels = json.load(g)
        experience = users[f'{user.id}']['experience']
        lvl_start = users[f'{user.id}']['level']
        lvl_end = int(experience ** (1 / 4))
        if lvl_start < lvl_end:
            print(user)
            print(user.id)
            print(users)
            await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}')
            users[f'{user.id}']['level'] = lvl_end

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

            embed = discord.Embed(
              title = "Level info",
              description = "Level:" + " " + lvl + "\nExperience" + " " + exp,
              color = discord.Color.dark_blue()
            )
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
