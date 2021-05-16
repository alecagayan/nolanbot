import discord
import asyncio
from discord.ext import commands
import sqlite3
import datetime
from os.path import isfile
from sqlite3 import connect


class Pets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def petsetup(self, ctx, *, pet):    
        DB_PATH = "./data/db/database.db"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        cur.execute(f"SELECT Pet FROM pets WHERE UserID = {ctx.message.author.id}")
        result = cur.fetchone()
        sql = ("INSERT INTO pets(UserID, Pet) VALUES(?,?)")
        val = (ctx.message.author.id, pet)
        await ctx.send(str(ctx.message.author.mention) + "'s pet has been set to " + pet)
        await ctx.send('Please run the `petphoto <petname>` command to add a photo!')

        cur.execute(sql, val)

        def check(m):
            return m.author == ctx.author

        cur.execute(f"SELECT Pet FROM pets WHERE UserID = {ctx.message.author.id}")
        result = cur.fetchone()
        if result is None:
            await ctx.send('Please set up a pet! use `!pethelp` to get some info!')

        if result is not None:
        
            await ctx.send('What type of pet do you have? (eg. Dog)?')
            msgType = await self.bot.wait_for('message', check=check)
            sqlType = ("UPDATE pets SET Type = ? WHERE Pet = ?")
            valType = (msgType.content, pet)


            await ctx.send('How old is your pet?')
            msgAge = await self.bot.wait_for('message', check=check)
            sqlAge = ("UPDATE pets SET Age = ? WHERE Pet = ?")
            valAge = (msgAge.content, pet)

        if result is not None:
            cur.execute(sqlType, valType)
            cur.execute(sqlAge, valAge)

        await ctx.send('Set!')
        
        db.commit()
        cur.close()
        db.close()

    @commands.command()
    async def rmpet(self, ctx, *, pet):
        DB_PATH = "./data/db/database.db"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        sqlDel = (f"DELETE FROM pets WHERE Pet = ? AND UserID = {ctx.message.author.id}")
        valDel = (pet)

        await ctx.send('Pet removed!')
        cur.execute(sqlDel, [valDel])
        db.commit()

        cur.close()
        db.close()



    @commands.command()
    async def petupdate(self, ctx, *, pet):

        DB_PATH = "./data/db/database.db"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        def check(m):
            return m.author == ctx.author

        cur.execute(f"SELECT Pet FROM pets WHERE UserID = {ctx.message.author.id}")
        result = cur.fetchone()
        if result is None:
            await ctx.send('Please set up a pet! use `!pethelp` to get some info!')

        if result is not None:
        
            await ctx.send('What type of pet do you have? (eg. Dog)?')
            msgType = await self.bot.wait_for('message', check=check)
            sqlType = ("UPDATE pets SET Type = ? WHERE Pet = ?")
            valType = (msgType.content, pet)


            await ctx.send('How old is your pet?')
            msgAge = await self.bot.wait_for('message', check=check)
            sqlAge = ("UPDATE pets SET Age = ? WHERE Pet = ?")
            valAge = (msgAge.content, pet)

        if result is not None:
            cur.execute(sqlType, valType)
            cur.execute(sqlAge, valAge)

        await ctx.send('Set!')
        db.commit()
        cur.close()
        db.close()

    @commands.command()
    async def petphoto(self, ctx, *, model):

        photo = ctx.message.attachments[0]
        DB_PATH = "./data/db/database.db"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        cur.execute(f"SELECT Pet FROM pets WHERE UserID = {ctx.message.author.id}")
        result = cur.fetchone()
        if result is None:
            await ctx.send('Please set up a pet! use `!pethelp` to get some info!')
        sql = ("UPDATE pets SET Photo = ? WHERE Pet = ?")
        val = (photo.url, model)

        if result is not None:
            cur.execute(sql, val)
        await ctx.send(str(ctx.message.author.mention) + "'s pet photo has been set to " + photo.url)

        db.commit()
        cur.close()
        db.close()

    @commands.command()
    async def pet(self, ctx, member: discord.Member = None):
        DB_PATH = "./data/db/database.db"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        if member is None:
            userid = ctx.message.author.id
        else:
            userid = member.id

        cur.execute("SELECT * FROM pets WHERE UserID=?", (userid,))
        rows = cur.fetchall()

        for row in rows:
            UserID = row[0]
            petname = row[1]
            petphoto = row[2]
            pettype = row[3]
            petage = row[4]

            embed = discord.Embed(title="Pet Info", description="Check out " + ''.join(petname) + "!", color=0xFFD414)

            if petname is not None:
                embed.add_field(name="Name", value=''.join(petname), inline=True)

            if pettype is not None:
                embed.add_field(name="Pet Type", value=''.join(pettype), inline=True)

            if petage is not None:
                embed.add_field(name="Age", value=''.join(petage), inline=True)

            if petphoto is not None:
                embed.set_image(url=''.join(petphoto))

            embed.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time
            await ctx.send(embed = embed)

        cur.close()
        db.close()

def setup(bot):
    bot.add_cog(Pets(bot))