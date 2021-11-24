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
                XPLock text
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
        if xpfetch is not None:
            lvl = xpfetch[0]
        else:
            lvl = 0
        cur.execute(f"SELECT XPLock FROM xp WHERE UserID = {message.author.id}")
        xplockfetch = cur.fetchone()
        if xplockfetch is not None:
            xplock = xplockfetch[0]
        else:
            xplock = ((datetime.utcnow()-timedelta(seconds=60)).isoformat())

        if datetime.utcnow() > datetime.fromisoformat(xplock):
            await self.add_xp(message, xp, lvl)

    async def add_xp(self, message, xp, lvl):
        xp_to_add = randint(10, 20)
        if xp == None:
            xp = 0
        if lvl == None:
            lvl = 0

        new_lvl = int(((int(xp)+xp_to_add)//42) ** 0.55)

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
            
            embed = discord.Embed(title="Server Level", description="Experience" , color=0xFFD414)
            embed.add_field(name="XP", value=str(xp), inline=True)
            embed.add_field(name="Level", value=str(lvl), inline=True)
            await ctx.send(embed = embed)
        else:
            await ctx.send("This user has no XP!")
        cur.close()
        db.close()

    # gets user with highest xp
    @commands.command()
    async def topxp(self, ctx):
        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        cur.execute("SELECT * FROM xp ORDER BY XP DESC LIMIT 10")
        res = cur.fetchall()

        await ctx.send(res)

        if len(res) != 0:
        
            for row in res:
                UserID = row[0]
                xp = row[1]
                lvl = row[2]
            
            embed = discord.Embed(title="Server Level", description="Experience" , color=0xFFD414)
            embed.add_field(name="XP", value=str(xp), inline=True)
            embed.add_field(name="Level", value=str(lvl), inline=True)
            await ctx.send(embed = embed)
        else:
            await ctx.send("No one has any XP!")
        cur.close()
        db.close()





def setup(bot):
    bot.add_cog(Xp(bot))
