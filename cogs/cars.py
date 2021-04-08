import discord
import asyncio
from discord.ext import commands
import sqlite3
from os.path import isfile
from sqlite3 import connect


class Cars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(invoke_without_command=True)
    async def cars(self, ctx):
        embed1 = discord.Embed(title="Available Setup Commands", description="Need help? Look below", color=embedColor)
        embed1.add_field(name=prefix + "helpme <tag or empty for info>", value='Get DU related help and answers to your questions!', inline=False)
        embed1.add_field(name=prefix + "vote", value="Makes a quick yes/no poll", inline=False)
        embed1.add_field(name=prefix + "covid <state or county> <name>", value="Gives coronavirus statistics", inline=False)
        embed1.add_field(name=prefix + "lyrics <song name/artist>", value="Prints song lyrics", inline=False)
        embed1.add_field(name=prefix + "servericon", value="Returns the server icon", inline=False)
        embed1.add_field(name=prefix + "quickpoll", value="Creates a quick poll with multiple options", inline=False)
        embed1.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time
        await ctx.send(embed=embed1)

    @commands.command()
    async def carsetup(self, ctx, *, model):
        DB_PATH = "./data/db/database.db"
        BUILD_PATH = "./data/db/build.sql"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        cur.execute(f"SELECT Car FROM database WHERE UserID = {ctx.message.author.id}")
        result = cur.fetchone()
        sql = ("INSERT INTO database(UserID, Car) VALUES(?,?)")
        val = (ctx.message.author.id, model)
        await ctx.send(str(ctx.message.author.id) + "'s car has been set to " + model)

        cur.execute(sql, val)
        db.commit()
        cur.close()
        db.close()

def setup(bot):
    bot.add_cog(Cars(bot))