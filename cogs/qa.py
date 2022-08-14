import discord
from discord.ext import commands

class QA(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='qa')
    async def qa(self, ctx, *, question):
        embed = discord.Embed(title=question, color=0xFFD414)
        #add user profile picture and name in "Sent by"
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        # send in specific channel'
        #channel
        channel = self.client.get_channel(1008189502780624997)
        await channel.send(embed=embed)

def setup(client):
    client.add_cog(QA(client))