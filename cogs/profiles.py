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
    async def pbio(self, ctx, *, bio)
        DB_PATH = "./data/db/database.db"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()
    
            if(len(bio) < 512):
            cur.execute(f"SELECT Bio FROM profiles WHERE UserID = {ctx.message.author.id}")
            result = cur.fetchone()

            sqlMods = ("UPDATE cars SET Mods = ? WHERE Car = ?")


        else:

    
    
def setup(bot):
    bot.add_cog(Profiles(bot))