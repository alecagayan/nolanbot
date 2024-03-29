import discord
from discord.ext import commands
import sqlite3
import random
from random import randint
from sqlite3 import connect
from datetime import datetime, timedelta


DB_PATH = "./data/db/xp.db"


class Xp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    db = connect(DB_PATH, check_same_thread=False)
    cur = db.cursor()

    cur.execute('''
                CREATE TABLE IF NOT EXISTS xp (
                UserID integer,
                XP text,
                Level integer,
                XPLock text,
                Permlevel integer
                );''')

    db.commit()
    cur.close()
    db.close()

    async def process_xp(self, message):

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        cur.execute(f"SELECT XP FROM xp WHERE UserID = {message.author.id}")
        xpfetch = cur.fetchone()
        if xpfetch is not None:
            xp = xpfetch[0]
        else:
            xp = 0
        cur.execute(f"SELECT Level FROM xp WHERE UserID = {message.author.id}")
        lvlfetch = cur.fetchone()
        if lvlfetch is not None:
            lvl = lvlfetch[0]
        else:
            lvl = 0
        cur.execute(
            f"SELECT XPLock FROM xp WHERE UserID = {message.author.id}")
        xplockfetch = cur.fetchone()
        cur.execute(
            f"SELECT Permlevel FROM xp WHERE UserID = {message.author.id}")
        permlevel = cur.fetchone()
        if permlevel is not None:
            permlevel = permlevel[0]
        if xplockfetch is not None:
            xplock = xplockfetch[0]
        else:
            xplock = ((datetime.utcnow()-timedelta(seconds=60)).isoformat())

        if datetime.utcnow() > datetime.fromisoformat(xplock):
            #check if message has more than 5 words, if not, don't add xp
            if len(message.content.split()) >= 5:
                await self.add_xp(message, xp, lvl, permlevel)

    async def add_xp(self, message, xp, lvl, permlevel):
        xp_to_add = randint(10, 15)
        if xp == None:
            xp = 0
        if lvl == None:
            lvl = 0
        if permlevel == None:
            permlevel = 0

        new_lvl = int(((int(xp)+xp_to_add)//42) ** 0.55)

        #add the increase in level to permlvl
        new_permlevel = int(permlevel) + (int(new_lvl)-int(lvl))

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        cur.execute(f"SELECT XP FROM xp WHERE UserID = {message.author.id}")

        check = cur.fetchone()

        if check is None:

            cur.execute("INSERT INTO xp(UserID, XP) VALUES(?,?)",
                        (message.author.id, 0))

        cur.execute(
            "UPDATE xp SET XP = ? WHERE UserID = ?", (int(xp) + xp_to_add, message.author.id))
        cur.execute(
            "UPDATE xp SET Level = ? WHERE UserID = ?", (new_lvl, message.author.id))
        cur.execute(
            "UPDATE xp SET XPLock = ? WHERE UserID = ?", (((datetime.utcnow()+timedelta(seconds=60)).isoformat()), message.author.id))
        cur.execute(
            "UPDATE xp SET Permlevel = ? WHERE UserID = ?", (new_permlevel, message.author.id))
        

        db.commit()
        cur.close()
        db.close()

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            await self.process_xp(message)

    @commands.command()
    async def xp(self, ctx, *, member: discord.Member = None):
        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        if member is None:
            idmember = ctx.message.author.id
        else:
            idmember = member.id

        cur.execute(f"SELECT * FROM xp WHERE UserID = {idmember}")
        res = cur.fetchall()

        if len(res) != 0:

            for row in res:
                UserID = row[0]
                xp = row[1]
                lvl = row[2]
                permlvl = row[4]


            embed = discord.Embed(title="Server Level",
                                  description="Experience", color=0xFFD414)
            embed.add_field(name="XP", value=str(xp), inline=True)
            embed.add_field(name="Level", value=str(lvl), inline=True)
            embed.add_field(name="Lifetime Total Level", value=str(permlvl), inline=True)

            await ctx.send(embed=embed)
        else:
            await ctx.send("This user has no XP!")
        cur.close()
        db.close()
    # get top 10 users with most xp

    @commands.command()
    async def top(self, ctx):
        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        cur.execute(
            "SELECT * FROM xp ORDER BY CAST(XP AS INTEGER) DESC LIMIT 10")
        res = cur.fetchall()

        if len(res) != 0:
            embed = discord.Embed(title="Server Level",
                                  description="Experience", color=0xFFD414)
            counter = 1
            for row in res:
                
                user = self.bot.get_user(row[0])
                xp = row[1]
                lvl = row[2]

                embed.add_field(name=str(counter) + ". " + user.name, value=str(xp), inline=False)
                counter+=1
            await ctx.send(embed=embed)
        else:
            await ctx.send("There are no users with XP!")
        cur.close()
        db.close()

    @commands.group()
    async def xpdb(self, ctx: commands.Context):  

        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid subcommand passed...')

    @xpdb.command(name="newcolumn")
    async def xpdb_newcolumn(self, ctx, *, column):

        if(ctx.author.id == 401063536618373121):

            db = connect(DB_PATH, check_same_thread=False)
            cur = db.cursor()

            cur.execute(f"ALTER TABLE xp ADD COLUMN {column} integer")
            db.commit()
            cur.close()
            db.close()

    @xpdb.command(name="copyvalues  ")
    async def copyvalues(self, ctx, col1, col2):
        if(ctx.author.id == 401063536618373121):

            #copies values from col1 to col2
            db = connect(DB_PATH, check_same_thread=False)
            cur = db.cursor()
            
            cur.execute(f"UPDATE xp SET {col2} = {col1}")
            db.commit()

            cur.close()
            db.close()

    @xpdb.command(name="xp0")
    async def xpdb_xp0(self, ctx):
        #set all values in XP column to 0
        if(ctx.author.id == 401063536618373121):
                
                db = connect(DB_PATH, check_same_thread=False)
                cur = db.cursor()
    
                cur.execute("UPDATE xp SET XP = 0")
                cur.execute("UPDATE xp SET Level = 0")

                db.commit()
    
                cur.close()
                db.close()

    @xpdb.command(name="rmuserxp")
    async def xpdb_rmuserxp(self, ctx, *, user: discord.Member):
        if(ctx.author.id == 401063536618373121):

            db = connect(DB_PATH, check_same_thread=False)
            cur = db.cursor()

            cur.execute(f"DELETE FROM xp WHERE UserID = {user.id}")
            db.commit()

            cur.close()
            db.close()

    @xpdb.command(name="setpermlvl")
    async def xpdb_setpermlvl(self, ctx, lvl, *, user: discord.Member):
        if(ctx.author.id == 401063536618373121):

            db = connect(DB_PATH, check_same_thread=False)
            cur = db.cursor()

            cur.execute(f"UPDATE xp SET Permlevel = {lvl} WHERE UserID = {user.id}")
            db.commit()

            cur.close()
            db.close()

    @xpdb.command(name="setxp")
    async def xpdb_setxp(self, ctx, xp, *, user: discord.Member):
        if(ctx.author.id == 401063536618373121):

            db = connect(DB_PATH, check_same_thread=False)
            cur = db.cursor()

            cur.execute(f"UPDATE xp SET XP = {xp} WHERE UserID = {user.id}")
            db.commit()

            cur.close()
            db.close()

    @xpdb.command(name="setlvl")
    async def xpdb_setlvl(self, ctx, lvl, *, user: discord.Member):
        if(ctx.author.id == 401063536618373121):

            db = connect(DB_PATH, check_same_thread=False)
            cur = db.cursor()

            cur.execute(f"UPDATE xp SET Level = {lvl} WHERE UserID = {user.id}")
            db.commit()

            cur.close()
            db.close()



def setup(bot):
    bot.add_cog(Xp(bot))
