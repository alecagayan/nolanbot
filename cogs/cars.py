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
        embed1.add_field(name="carupdate <same make and model as setup>", value="Add info about your car to the database", inline=False)
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
    async def carupdate(self, ctx, *, model):

        DB_PATH = "./data/db/database.db"
        BUILD_PATH = "./data/db/build.sql"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        def check(m):
            return m.author == ctx.author

        cur.execute(f"SELECT Car FROM cars WHERE UserID = {ctx.message.author.id}")
        result = cur.fetchone()
        if result is None:
            await ctx.send('Please set up a car! use `!carhelp` to get some info!')

        if result is not None:
        
            await ctx.send('Which model year is your car?')
            msgYear = await self.bot.wait_for('message', check=check)
            print(msgYear.content)
            sqlYear = ("UPDATE cars SET Year = ? WHERE Car = ?")
            valYear = (msgYear.content, model)
            print(valYear)

            await ctx.send('Which color is your car?')
            msgColor = await self.bot.wait_for('message', check=check)
            sqlColor = ("UPDATE cars SET Color = ? WHERE Car = ?")
            valColor = (msgColor.content, model)

            await ctx.send('How many miles does your car have?')
            msgMiles = await self.bot.wait_for('message', check=check)
            sqlMiles = ("UPDATE cars SET Miles = ? WHERE Car = ?")
            valMiles = (msgMiles.content, model)

            await ctx.send('Which mods have you done to your car? Separate them with a comma!')
            msgMods = await self.bot.wait_for('message', check=check)
            sqlMods = ("UPDATE cars SET Mods = ? WHERE Car = ?")
            valMods = (msgMods.content, model)

        if result is not None:
            cur.execute(sqlYear, valYear)
            print(valYear)
            cur.execute(sqlColor, valColor)
            cur.execute(sqlMiles, valMiles)
            cur.execute(sqlMods, valMods)

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

        cur.execute(f"SELECT Car FROM cars WHERE UserID = {userid}")
        makeandmodel = cur.fetchone()

        

        embed = discord.Embed(title="Car Info", description="Check out this " + ''.join(makeandmodel) + "!", color=0xFFD414)


        if makeandmodel[0] is not None:
            embed.add_field(name="Make and Model", value=''.join(makeandmodel), inline=True)

        
        cur.execute(f"SELECT Year FROM cars WHERE UserID = {userid}")
        modelyear = cur.fetchone()
        print(modelyear)
        print(type(modelyear))
        if modelyear[0] is not None:
            embed.add_field(name="Model Year", value=''.join(modelyear), inline=True)

        cur.execute(f"SELECT Color FROM cars WHERE UserID = {userid}")
        carcolor = cur.fetchone()
        if carcolor[0] is not None:
            embed.add_field(name="Color", value=''.join(carcolor), inline=True)

        cur.execute(f"SELECT Miles FROM cars WHERE UserID = {userid}")
        carmiles = cur.fetchone()
        if carmiles[0] is not None:
            embed.add_field(name="Mileage", value=''.join(carmiles), inline=True)

        cur.execute(f"SELECT Mods FROM cars WHERE UserID = {userid}")
        carmods = cur.fetchone()
        if carmods[0] is not None:
            embed.add_field(name="Mods", value=''.join(carmods), inline=True)

        cur.execute(f"SELECT Photo FROM cars WHERE UserID = {userid}")
        carphoto = cur.fetchone()
        if carphoto[0] is not None:
            embed.set_image(url=''.join(carphoto))

        embed.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time        db.commit()
        await ctx.send(embed = embed)
        cur.close()
        db.close()

def setup(bot):
    bot.add_cog(Cars(bot))