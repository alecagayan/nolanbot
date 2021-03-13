import discord
from discord.ext import commands

class Helpme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def helpme(self, ctx, tag):
        if(tag == 'sticker'):
            await ctx.send('Check out <#788841099325079622> for all your sticker related questions!')

def setup(bot):
    bot.add_cog(Helpme(bot))