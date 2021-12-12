import discord
import asyncio
from discord.ext import commands
import sqlite3
import datetime
from os.path import isfile
from sqlite3 import connect

pretendID = 0

class Cars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def carhelp(self, ctx):
        embed1 = discord.Embed(title="Available Setup Commands", description="Need help? Look below", color=0xFFD414)
        embed1.add_field(name="carsetup <make and model>", value="Add your car's make and model to the database", inline=False)
        embed1.add_field(name="carphoto <same make and model as setup> <photo>", value="Add a photo to the car database", inline=False)
        embed1.add_field(name="carupdate <same make and model as setup>", value="Add info about your car to the database", inline=False)
        embed1.add_field(name="car <member/none>", value="Look up your own or someone else's car!", inline=False)
        embed1.add_field(name="rmcar <make and model>", value="Removes your car from the database", inline=False)
        embed1.add_field(name="STEP BY STEP INSTRUCTIONS", value="Step 1: run `carsetup <make and model> ", inline=False)

    @commands.slash_command()
    async def pretend(self, ctx, id):
        global pretendID
        pretendID = id
        print(pretendID)

    @commands.slash_command()
    async def carsetup(self, ctx, *, model = None):    
        DB_PATH = "./data/db/database.db"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        userid = ctx.message.author.id

        if pretendID != 0 and ctx.message.author.id == 401063536618373121:
            userid = pretendID

        if model is not None:

            cur.execute(f"SELECT Car FROM cars WHERE UserID = {userid}")
            result = cur.fetchone()
            sql = ("INSERT INTO cars(UserID, Car) VALUES(?,?)")
            val = (ctx.message.author.id, model)
            await ctx.respond(str(ctx.message.author.mention) + "'s car has been set to " + model)
            cur.execute(sql, val)



            def check(m):
                return m.author == ctx.author

            cur.execute(f"SELECT Car FROM cars WHERE UserID = {userid}")
            result = cur.fetchone()
            if result is None:
                await ctx.respond('Please set up a car! use `!carhelp` to get some info!')

            if result is not None:
            
                await ctx.respond('Which model year is your car?')
                msgYear = await self.bot.wait_for('message', check=check)
                sqlYear = (f"UPDATE cars SET Year = ? WHERE Car = ? AND UserID = {pretendID}")
                valYear = (msgYear.content, model)

                await ctx.respond('Which color is your car?')
                msgColor = await self.bot.wait_for('message', check=check)
                sqlColor = (f"UPDATE cars SET Color = ? WHERE Car = ? AND UserID = {userid}")
                valColor = (msgColor.content, model)

                await ctx.respond('How many miles does your car have?')
                msgMiles = await self.bot.wait_for('message', check=check)
                sqlMiles = (f"UPDATE cars SET Miles = ? WHERE Car = ? AND UserID = {userid}")
                valMiles = (msgMiles.content, model)

                await ctx.respond('Which mods have you done to your car? Separate them with a comma!')
                msgMods = await self.bot.wait_for('message', check=check)
                sqlMods = (f"UPDATE cars SET Mods = ? WHERE Car = ? AND UserID = {userid}")
                valMods = (msgMods.content, model)

            if result is not None:
                cur.execute(sqlYear, valYear)
                cur.execute(sqlColor, valColor)
                cur.execute(sqlMiles, valMiles)
                cur.execute(sqlMods, valMods)

            await ctx.respond('Set!')
            await ctx.respond('Please run the `carphoto <make and model>` command to add a photo!')


            db.commit()
        else:
            await ctx.respond("**Check out the wiki for instructions on how to set up your car: https://wiki.nolanbot.xyz/wiki/Database_Commands**")
        cur.close()
        db.close()

    
    @commands.slash_command()
    async def rmcar(self, ctx, *, model = None):
        DB_PATH = "./data/db/database.db"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        userid = ctx.message.author.id

        if pretendID != 0 and ctx.message.author.id == 401063536618373121:
            userid = pretendID        

        if model is not None:

            sqlDel = (f"DELETE FROM cars WHERE Car = ? AND UserID = {userid}")
            valDel = (model)

            await ctx.respond('Car removed!')
            cur.execute(sqlDel, [valDel])
            db.commit()
        else:
            await ctx.respond("**Check out the wiki for instructions on how to remove your car: https://wiki.nolanbot.xyz/wiki/Database_Commands**")
        cur.close()
        db.close()

    @commands.slash_command()
    async def carmembers(self, ctx):
        DB_PATH = "./data/db/database.db"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        carmembers = [car[0] for car in cur.execute("SELECT UserID FROM cars")]

        await ctx.respond(carmembers)

    @commands.slash_command()
    async def carupdate(self, ctx, *, model = None):

        DB_PATH = "./data/db/database.db"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        userid = ctx.message.author.id

        if pretendID != 0 and ctx.message.author.id == 401063536618373121:
            userid = pretendID

        def check(m):
            return m.author == ctx.author

        if model is not None:

            cur.execute(f"SELECT Car FROM cars WHERE UserID = {userid}")
            result = cur.fetchone()
            if result is None:
                await ctx.respond('Please set up a car! use `!carhelp` to get some info!')

            if result is not None:
            
                await ctx.respond('Which model year is your car?')
                msgYear = await self.bot.wait_for('message', check=check)
                print(msgYear.content)
                sqlYear = (f"UPDATE cars SET Year = ? WHERE Car = ? AND UserID = {userid}")
                valYear = (msgYear.content, model)
                print(valYear)

                await ctx.respond('Which color is your car?')
                msgColor = await self.bot.wait_for('message', check=check)
                sqlColor = (f"UPDATE cars SET Color = ? WHERE Car = ? AND UserID = {userid}")
                valColor = (msgColor.content, model)

                await ctx.respond('How many miles does your car have?')
                msgMiles = await self.bot.wait_for('message', check=check)
                sqlMiles = (f"UPDATE cars SET Miles = ? WHERE Car = ? AND UserID = {userid}")
                valMiles = (msgMiles.content, model)

                await ctx.respond('Which mods have you done to your car? Separate them with a comma!')
                msgMods = await self.bot.wait_for('message', check=check)
                sqlMods = (f"UPDATE cars SET Mods = ? WHERE Car = ? AND UserID = {userid}")
                valMods = (msgMods.content, model)

            if result is not None:
                cur.execute(sqlYear, valYear)
                cur.execute(sqlColor, valColor)
                cur.execute(sqlMiles, valMiles)
                cur.execute(sqlMods, valMods)

            await ctx.respond('Set!')
            db.commit()

        else:
            await ctx.respond("**Check out the wiki for instructions on how to update your car: https://wiki.nolanbot.xyz/wiki/Database_Commands**")
        cur.close()
        db.close()

    @commands.slash_command()
    async def carphoto(self, ctx, *, model = None):

        DB_PATH = "./data/db/database.db"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        if model is not None:
            if ctx.message.attachments[0] is not None:
                photo = ctx.message.attachments[0]
            else:
                await ctx.respond("**Make sure to attach a photo. More info at: https://wiki.nolanbot.xyz/wiki/Database_Commands**")

        userid = ctx.message.author.id

        if pretendID != 0 and ctx.message.author.id == 401063536618373121:
            userid = pretendID

        cur.execute(f"SELECT Car FROM cars WHERE UserID = {userid}")
        result = cur.fetchone()
        if result is None:
            await ctx.respond('Please set up a car! use `!carhelp` to get some info!')
        sql = (f"UPDATE cars SET Photo = ? WHERE Car = ? AND UserID = {userid}")
        val = (photo.url, model)

        if result is not None:
            cur.execute(sql, val)
            await ctx.respond(str(ctx.message.author.mention) + "'s car photo has been set to " + photo.url)
        else:
            await ctx.respond("**Check out the wiki for instructions on how to set or update your car photo: https://wiki.nolanbot.xyz/wiki/Database_Commands**")

        db.commit()

      
        cur.close()
        db.close()


    @commands.slash_command()
    async def dreamcar(self, ctx, *, model):
        DB_PATH = "./data/db/database.db"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        userid = ctx.message.author.id

        if pretendID != 0 and ctx.message.author.id == 401063536618373121:
            userid = pretendID

        cur.execute(f"SELECT Car FROM cars WHERE UserID = {userid}")
        result = cur.fetchone()

        if result is not None:
            sql = (f"UPDATE cars SET Extra1 = ? WHERE UserID = {userid}")
            val = (model,)
            cur.execute(sql, val)
            
            await ctx.respond("Set!")
        db.commit()
        cur.close()
        db.close()

    @commands.slash_command()
    async def car(self, ctx, member: discord.Member = None, *, model = None):
        DB_PATH = "./data/db/database.db"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()
        print(pretendID)

        if member is None:
            user = ctx.message.author
            userid = ctx.message.author.id
        else:
            userid = member.id

            user = member

        if pretendID != 0 and ctx.message.author.id == 401063536618373121:
            userid = pretendID
        if model is None:
            cur.execute("SELECT * FROM cars WHERE UserID=?", (userid,))
        else:
            cur.execute("SELECT * FROM cars WHERE UserID=? AND Car = ?", (userid, model))

        rows = cur.fetchall()

        dreamcar = None

        for row in rows:
            UserID = row[0]
            carmake = row[1]
            carphoto = row[2]
            carcolor = row[3]
            caryear = row[4]
            carmiles = row[5]
            carmods = row[6]
            dreamcar = row[7]

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
            await ctx.respond(embed = embed)


        cur.close()
        db.close()
        if dreamcar is not None:
            await ctx.respond(user.display_name + "'s dream car is a: " + ''.join(dreamcar))


    @commands.slash_command()
    async def carcount(self, ctx):
        DB_PATH = "./data/db/database.db"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        cur.execute("SELECT * FROM cars")
        rows = cur.fetchall()

      #counts the number of rows in the table
        count = 0
        for row in rows:
            count += 1

        await ctx.respond("There are " + str(count) + " cars in the database!")

        cur.close()
        db.close()

    @commands.command(name='drives', aliases=['owns', 'whohas'])
    async def drives(self, ctx, *, model = None):
        if model is None:
            await ctx.respond("Please specify a car!")
            return

        DB_PATH = "./data/db/database.db"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        sql = (f"""
            SELECT *
            FROM cars
            WHERE Car LIKE '%{model}%'
            LIMIT 10;
        """)
        cur.execute(sql)
        rows = cur.fetchall()

        if len(rows) == 0:
            await ctx.respond("Sorry, no one has said they drive that car!")
            return

        for row in rows:
            UserID = row[0]
            carmake = row[1]
            carphoto = row[2]
            carcolor = row[3]
            caryear = row[4]
            carmiles = row[5]

            user = await self.bot.fetch_user(UserID)
            title = ''.join(user.name) + "'s "
            if caryear is not None:
                caryear = caryear.replace('!carsetup', '')
                if caryear not in carmake:
                    title += ''.join(caryear.strip()) + " "
            title += ''.join(carmake)
            if carmiles is not None:
                carmiles = ''.join(carmiles)
            else:
                carmiles = "None Provided"
            embed = discord.Embed(
                title=title, description='Mileage: ' + ''.join(carmiles),
                color=0xFFD414
            )

            if carphoto is not None:
                embed.set_thumbnail(url=''.join(carphoto))

            if carcolor is not None:
                embed.add_field(name="Color", value=''.join(carcolor), inline=True)

            await ctx.respond(embed = embed)

        cur.close()
        db.close()
        
def setup(bot):
    bot.add_cog(Cars(bot))
