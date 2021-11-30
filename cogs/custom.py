import discord
from discord.ext import commands
import asyncio
import random

class Custom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sav(self, ctx, *, args):
        # send youtube link
        await ctx.send('https://youtu.be/Qll7IHN0I4Q')

def setup(bot):
    bot.add_cog(Custom(bot))