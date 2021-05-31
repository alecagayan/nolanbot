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
        embed1.add_field(name="rmcar <make and model>", value="Removes your car from the database", inline=False)
        embed1.add_field(name="STEP BY STEP INSTRUCTIONS", value="Step 1: run `carsetup <make and model> ", inline=False)

    @commands.command()
    async def carsetup(self, ctx, *, model = None):    
        DB_PATH = "./data/db/database.db"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        if model is not None:

            cur.execute(f"SELECT Car FROM cars WHERE UserID = {ctx.message.author.id}")
            result = cur.fetchone()
            sql = ("INSERT INTO cars(UserID, Car) VALUES(?,?)")
            val = (ctx.message.author.id, model)
            await ctx.send(str(ctx.message.author.mention) + "'s car has been set to " + model)
            await ctx.send('Please run the `carphoto <make and model>` command to add a photo!')

            cur.execute(sql, val)

            def check(m):
                return m.author == ctx.author

            cur.execute(f"SELECT Car FROM cars WHERE UserID = {ctx.message.author.id}")
            result = cur.fetchone()
            if result is None:
                await ctx.send('Please set up a car! use `!carhelp` to get some info!')

            if result is not None:
            
                await ctx.send('Which model year is your car?')
                msgYear = await self.bot.wait_for('message', check=check)
                sqlYear = ("UPDATE cars SET Year = ? WHERE Car = ?")
                valYear = (msgYear.content, model)

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
                cur.execute(sqlColor, valColor)
                cur.execute(sqlMiles, valMiles)
                cur.execute(sqlMods, valMods)

            await ctx.send('Set!')

            db.commit()
        else:
            await ctx.send("**Check out the wiki for instructions on how to set up your car: https://wiki.nolanbot.xyz/wiki/Database_Commands**")
        cur.close()
        db.close()

    
    @commands.command()
    async def rmcar(self, ctx, *, model = None):
        DB_PATH = "./data/db/database.db"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        if model is not None:

            sqlDel = (f"DELETE FROM cars WHERE Car = ? AND UserID = {ctx.message.author.id}")
            valDel = (model)

            await ctx.send('Car removed!')
            cur.execute(sqlDel, [valDel])
            db.commit()
        else:
            await ctx.send("**Check out the wiki for instructions on how to remove your car: https://wiki.nolanbot.xyz/wiki/Database_Commands**")
        cur.close()
        db.close()

    @commands.command()
    async def carmembers(self, ctx):
        DB_PATH = "./data/db/database.db"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        carmembers = [car[0] for car in cur.execute("SELECT UserID FROM cars")]

        await ctx.send(carmembers)

    @commands.command()
    async def carupdate(self, ctx, *, model = None):

        DB_PATH = "./data/db/database.db"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        def check(m):
            return m.author == ctx.author

        if model is not None:

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
                sqlMods = (f"UPDATE cars SET Mods = ? WHERE Car = ? AND UserID = {ctx.message.author.id}")
                valMods = (msgMods.content, model)

            if result is not None:
                cur.execute(sqlYear, valYear)
                cur.execute(sqlColor, valColor)
                cur.execute(sqlMiles, valMiles)
                cur.execute(sqlMods, valMods)

            await ctx.send('Set!')
            db.commit()

        else:
            await ctx.send("**Check out the wiki for instructions on how to update your car: https://wiki.nolanbot.xyz/wiki/Database_Commands**")
        cur.close()
        db.close()

    @commands.command()
    async def carphoto(self, ctx, *, model = None):

        DB_PATH = "./data/db/database.db"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        if model is not None:
            if ctx.message.attachments[0] is not None:
                photo = ctx.message.attachments[0]
            else:
                await ctx.send("**Make sure to attach a photo. More info at: https://wiki.nolanbot.xyz/wiki/Database_Commands**")


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

        else:
            await ctx.send("**Check out the wiki for instructions on how to set or update your car photo: https://wiki.nolanbot.xyz/wiki/Database_Commands**")
        cur.close()
        db.close()

    @commands.command()
    async def car(self, ctx, member: discord.Member = None):
        DB_PATH = "./data/db/database.db"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        if member is None:
            userid = ctx.message.author.id
        else:
            userid = member.id

        cur.execute("SELECT * FROM cars WHERE UserID=?", (userid,))
        rows = cur.fetchall()

        for row in rows:
            UserID = row[0]
            carmake = row[1]
            carphoto = row[2]
            carcolor = row[3]
            caryear = row[4]
            carmiles = row[5]
            carmods = row[6]

            embed = discord.Embed(title="Car Info", description="Check out this " + ''.join(carmake) + "!", color=0xFFD414)

            if carmake is not None:
                embed.add_field(name="Make and Model", value=''.join(carmake), inline=True)

            if caryear is not None:
                embed.add_field(name="Model Year", value=''.join(caryear), inline=True)

            if carcolor is not None:
                embed.add_field(name="Color", value=''.join(carcolor), inline=True)

            if carmiles is not None:
                embed.add_field(name="Mileage", value=''.join(carmiles), inline=True)

            if carmods is not None:
                embed.add_field(name="Mods", value=''.join(carmods), inline=True)

            if carphoto is not None:
                embed.set_image(url=''.join(carphoto))

            embed.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time
            await ctx.send(embed = embed)

        cur.close()
        db.close()

def setup(bot):
    bot.add_cog(Cars(bot))