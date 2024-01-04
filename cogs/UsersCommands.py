import discord
from discord.ext import commands
from typing import Optional
from mcstatus import JavaServer, BedrockServer


class MinecraftInfo:
    def __init__(self, ip, port, version):
        self.ip = ip
        self.port = port
        self.version = version.strip().lower()

    def getJavaServerState(self):
        if self.version == "java":
            try:
                print(self.ip, self.port, self.version)
                server = JavaServer.lookup(f"{str(self.ip)}:{str(self.port)}")

                j_online = server.status().players.online
                j_latency = server.status().latency

                return j_online, j_latency
            except:
                return None, None
        else:
            return None, None

    def getBedrockServerState(self):
        if self.version == "bedrock":
            try:
                server = BedrockServer.lookup(
                    f"{str(self.ip)}:{str(self.port)}")

                b_online = server.status().players.online
                b_latency = server.status().latency

                return b_online, b_latency
            except:
                return None, None
        else:
            return None, None


class UsersCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # >> Clear Messages
    @commands.command(name="clear")
    async def clear(self, ctx, amount: Optional[int] = 1, showtext=None):
        await ctx.channel.purge(limit=amount + 1)
        if showtext is None:
            await ctx.send(f'*Delete {amount} message(s)*')
        elif showtext == "None" or "none":
            pass
        else:
            await ctx.send(f'*Deleted {amount} message(s)*')

    # >> Sending a fight challenge to others
    @commands.command(name="fight", aliases=["隻抽"])
    async def fight(self, ctx, user: discord.Member):
        embed = discord.Embed(title="隻抽 challenge",
                              description=user.mention + " " +
                              ctx.author.mention + " wants 隻抽 with you!")
        await ctx.reply(embed=embed)
        # await ctx.message.delete()

    # >> Exile other people to 西伯利亞
    @commands.command(name="exile")
    async def exile(self, ctx, user: discord.Member):
        channel = discord.utils.get(ctx.guild.voice_channels, name="西伯利亞")
        # print(channel)
        await user.move_to(channel)
        embed = discord.Embed(description=user.mention +
                              " has been exiled to 西伯利亞",
                              color=discord.Color.dark_blue())
        await ctx.send(embed=embed)

    @commands.command(name="mc")
    async def mc(self, ctx, ip, port=25565, version="java"):

        mc_server = MinecraftInfo(ip, port, version)

        j_online, j_latency = mc_server.getJavaServerState()
        b_online, b_latency = mc_server.getBedrockServerState()

        if j_online != None or j_latency != None:
            embed = discord.Embed(
                title="Server Info:",
                description=
                f"Server IP: {ip} \nPort: {port}\nPlayer Online: {j_online} \nLatency: {round(j_latency, 2)}ms",
                color=discord.Color.dark_blue())
            embed.set_thumbnail(
                url=
                "https://i1.wp.com/www.craftycreations.net/wp-content/uploads/2019/08/Grass-Block-e1566147655539.png?fit=500%2C500&ssl=1"
            )
            await ctx.send(embed=embed)

            if b_online != None or b_latency != None:
                embed = discord.Embed(
                    title="Server Info:",
                    description=
                    f"Server IP: {ip} \nPort: {port} \nPlayer Online: {b_online} \nLatency: {round(b_latency, 2)}ms",
                    color=discord.Color.dark_blue())
                embed.set_thumbnail(
                    url=
                    "https://i1.wp.com/www.craftycreations.net/wp-content/uploads/2019/08/Grass-Block-e1566147655539.png?fit=500%2C500&ssl=1"
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                description="Server IP or port is wrong! Please try again!")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(UsersCommands(bot))
