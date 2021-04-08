import discord
import asyncio
from discord.ext import commands


class Cars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def cars(self, ctx):
        await ctx.send('Available setup commands: \neofwh \nweoufwfe \nweubwof')



def setup(bot):
    bot.add_cog(Cars(bot))