import discord
from discord.ext import commands
import json


class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open("lvl_data/users.json", 'r') as f:
            users = json.load(f)

        await self.update_data(users, member)

        with open('lvl_data/users.json', 'w') as f:
            json.dump(users, f)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == False:
            with open('lvl_data/users.json', 'r') as f:
                users = json.load(f)

            await self.update_data(users, message.author)
            await self.add_experience(users, message.author, 5)
            await self.level_up(users, message.author, message)

            with open('lvl_data/users.json', 'w') as f:
                json.dump(users, f)

    async def update_data(self, users, user):
        if not f'{user.id}' in users:
            users[f'{user.id}'] = {}
            users[f'{user.id}']['experience'] = 0
            users[f'{user.id}']['level'] = 1

    async def add_experience(self, users, user, exp):
        users[f'{user.id}']['experience'] += exp

    async def level_up(self, users, user, message):
        with open('lvl_data/levels.json', 'r') as g:
          levels = json.load(g)
        experience = users[f'{user.id}']['experience']
        lvl_start = users[f'{user.id}']['level']
        lvl_end = int(experience ** (1 / 4))
        if lvl_start < lvl_end:
            embed = discord.Embed(title="**LEVEL UP!**",
                                  description=f'{user.mention} has leveled up to level {lvl_end}! :fire: 'f'\n Soundwave Superior,{user.mention} Inferior ',
                                  color=discord.Color.dark_red())
            embed.set_thumbnail(url=user.avatar_url)
            users[f'{user.id}']['level'] = lvl_end
            await message.channel.send(embed=embed)
  
    @commands.command()
    async def level(self, ctx, member: discord.Member = None):
        if not member:
            id = ctx.message.author.id
            with open('lvl_data/users.json', 'r') as f:
                users = json.load(f)
              
            lvl = users[str(id)]['level']
            exp = str(users[str(id)]['experience'])
          
            name = ctx.message.author
            url = name.avatar_url

            embed = discord.Embed(
              title = "Level info",
              description = "Level: " + str(lvl) + "\nExperience: " + str(exp),
              color = discord.Color.dark_blue()
            )
            embed.set_thumbnail(url=url)

            await ctx.send(name.mention + " " + f'is now level {lvl}!')
            #print(ctx.message.author.name)
            await ctx.send(embed=embed)
        else:
            id = member.id
            with open('lvl_data/users.json', 'r') as f:
                users = json.load(f)
            lvl = users[str(id)]['level']
            await ctx.send(f'{member} is at level {lvl}!')

def setup(bot):
  bot.add_cog(LevelSystem(bot))
  
