import discord
import asyncio
from discord.ext import commands
import sqlite3
import datetime
from os.path import isfile
from sqlite3 import connect


class Cars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def carhelp(self, ctx):
        embed1 = discord.Embed(title="Available Setup Commands", description="Need help? Look below", color=0xFFD414)
        embed1.add_field(name="carsetup <make and model>", value="Add your car's make and model to the database", inline=False)
        embed1.add_field(name="carphoto <same make and model as setup> <photo>", value="Add a photo to the car database", inline=False)
        embed1.add_field(name="carupdate <same make and model as setup> <color/year/mods/miles> <value>", value="Add info about your car to the database", inline=False)
        embed1.add_field(name="car <member/none>", value="Look up your own or someone else's car!", inline=False)
        embed1.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time
        await ctx.send(embed=embed1)

    @commands.command()
    async def carsetup(self, ctx, *, model):    
        DB_PATH = "./data/db/database.db"
        BUILD_PATH = "./data/db/build.sql"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        cur.execute(f"SELECT Car FROM cars WHERE UserID = {ctx.message.author.id}")
        result = cur.fetchone()
        sql = ("INSERT INTO cars(UserID, Car) VALUES(?,?)")
        val = (ctx.message.author.id, model)
        await ctx.send(str(ctx.message.author.mention) + "'s car has been set to " + model)
        await ctx.send('Please run the `carphoto <make and model>` command to add a photo!')

        cur.execute(sql, val)
        db.commit()
        cur.close()
        db.close()

    @commands.command()
    async def carupdate(self, ctx, model, field, *, mod, ):

        DB_PATH = "./data/db/database.db"
        BUILD_PATH = "./data/db/build.sql"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        cur.execute(f"SELECT Car FROM cars WHERE UserID = {ctx.message.author.id}")
        result = cur.fetchone()
        if result is None:
            await ctx.send('Please set up a car! use `!carhelp` to get some info!')
        
        if field == 'color':
            sql = ("UPDATE cars SET Color = ? WHERE Car = ?")
            val = (mod, model)
        if field == 'year':
            sql = ("UPDATE cars SET Year = ? WHERE Car = ?")
            val = (mod, model)
        if field == 'mods':
            sql = ("UPDATE cars SET Mods = ? WHERE Car = ?")
            val = (mod, model)
        if field == 'miles':
            sql = ("UPDATE cars SET Miles = ? WHERE Car = ?")
            val = (mod, model)

        if result is not None:
            cur.execute(sql, val)
        await ctx.send('Set!')
        db.commit()
        cur.close()
        db.close()

    @commands.command()
    async def carphoto(self, ctx, *, model):

        photo = ctx.message.attachments[0]
        DB_PATH = "./data/db/database.db"
        BUILD_PATH = "./data/db/build.sql"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        cur.execute(f"SELECT Car FROM cars WHERE UserID = {ctx.message.author.id}")
        result = cur.fetchone()
        if result is None:
            await ctx.send('Please set up a car! use `!carhelp` to get some info!')
        sql = ("UPDATE cars SET Photo = ? WHERE Car = ?")
        val = (photo.url, model)
        await ctx.send(str(ctx.message.author.mention) + "'s car photo has been set to " + photo.url)

        if result is not None:
            cur.execute(sql, val)
        await ctx.send(str(ctx.message.author.mention) + "'s car photo has been set to " + photo.url)

        db.commit()
        cur.close()
        db.close()

    @commands.command()
    async def car(self, ctx, member: discord.Member = None):
        DB_PATH = "./data/db/database.db"
        BUILD_PATH = "./data/db/build.sql"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        if member is None:
            userid = ctx.message.author.id
        else:
            userid = member.id

        cur.execute("SELECT * FROM cars WHERE UserID=?", (userid,))
        rows = cur.fetchall()

        for row in rows:
            await ctx.send(row)

        embed = discord.Embed(title="Available Setup Commands", description="Need help? Look below", color=embedColor)

        db.commit()
        cur.close()
        db.close()

def setup(bot):
    bot.add_cog(Cars(bot))