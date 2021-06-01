import discord
import asyncio
from discord.ext import commands
import sqlite3
import datetime
from os.path import isfile
from sqlite3 import connect


class Profiles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def psetup(self, ctx, *, name = None):    
        DB_PATH = "./data/db/database.db"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        cur.execute(f"SELECT Name FROM profiles WHERE UserID = {ctx.message.author.id}")
        result = cur.fetchone()

        if result is None:
            sql = ("INSERT INTO profiles(UserID, Name) VALUES(?,?)")
            val = (ctx.message.author.id, name)
            cur.execute(sql, val)
            db.commit()
        cur.close()
        db.close()
    
    @commands.command()
    async def pbio(self, ctx, *, bio):
        DB_PATH = "./data/db/database.db"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()
    
        if(len(bio) < 512):

            sql = (f"UPDATE profiles SET Bio = ? WHERE UserID = {ctx.message.author.id}")
            val = (bio,)
            cur.execute(sql, val)
            db.commit()
        cur.close()
        db.close()

    @commands.command(aliases=['pronouns'])
    async def ppronouns(self, ctx, *, bio):
        DB_PATH = "./data/db/database.db"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()
    
        if(len(bio) < 512):

            sql = (f"UPDATE profiles SET Pronouns = ? WHERE UserID = {ctx.message.author.id}")
            val = (bio,)
            cur.execute(sql, val)
            db.commit()
        cur.close()
        db.close()

    
    @commands.command()
    async def plink(self, ctx, *, link):
        DB_PATH = "./data/db/database.db"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()
    
        if(len(link) < 256):

            sql = (f"UPDATE profiles SET Extra1 = ? WHERE UserID = {ctx.message.author.id}")
            val = (link,)
            cur.execute(sql, val)
            db.commit()
        cur.close()
        db.close()

    @commands.command(aliases=['p'])
    async def profile(self, ctx, member: discord.Member = None):
        DB_PATH = "./data/db/database.db"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        if member is None:
            userid = ctx.message.author.id
        else:
            userid = member.id

        cur.execute("SELECT * FROM profiles WHERE UserID=?", (userid,))
        rows = cur.fetchall()

        for row in rows:
            UserID = row[0]
            name = row[1]
            bio = row[2]
            pronouns = row[3]
            link = row[4]

            embed = discord.Embed(title="Pet Info", description="not sure what to put here", color=0xFFD414)

            if name is not None:
                embed.add_field(name="Name", value=''.join(name), inline=True)

            if pronouns is not None:
                embed.add_field(name="Pronouns", value=''.join(pronouns), inline=True)

            if bio is not None:
                embed.add_field(name="Bio", value=''.join(bio), inline=True)

            if link is not None:
                embed.add_field(name="Bio", value=''.join(link), inline=True)


            embed.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time
            await ctx.send(embed = embed)

        cur.close()
        db.close()


    
    
def setup(bot):
    bot.add_cog(Profiles(bot))