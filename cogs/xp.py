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

    print("hi2")


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
        if cur.fetchone() is not None:
            xp = cur.fetchone()[0]
        else:
            xp = 0
        cur.execute(f"SELECT Level FROM xp WHERE UserID = {message.author.id}")
        if cur.fetchone() is not None:
            lvl = cur.fetchone()[0]
        else:
            lvl = 0
        cur.execute(f"SELECT XPLock FROM xp WHERE UserID = {message.author.id}")
        if cur.fetchone() is not None:
            xplock = cur.fetchone()[0]
        else:
            xplock = ((datetime.utcnow()+timedelta(seconds=60)).isoformat())

        print(xp)
        print(lvl)
        print(xplock)

        if datetime.utcnow() > datetime.fromisoformat(xplock):
            await self.add_xp(message, xp, lvl)



    async def add_xp(self, message, xp, lvl):
        xp_to_add = randint(10, 20)
        if xp == None:
            xp = 0
        if lvl == None:
            lvl = 0
        print("")
        print(xp)
        print(lvl)
        new_lvl = int(((int(xp)+xp_to_add)//42) ** 0.55)

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        cur.execute(f"SELECT XP FROM xp WHERE UserID = {message.author.id}")

        check = cur.fetchone()
        print(check)

        if check is None:
            print("inserting")
            cur.execute("INSERT INTO xp(UserID, XP) VALUES(?,?)", (message.author.id, 0))

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
            print("debug1")
            await self.process_xp(message)


def setup(bot):
    bot.add_cog(Xp(bot))
