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
    async def carhelp(self, ctx):
        embed1 = discord.Embed(title="Available Setup Commands", description="Need help? Look below", color=0xFFD414)
        embed1.add_field(name="carsetup <make and model>", value="Add your car's make and model to the database", inline=False)
        embed1.add_field(name="carphoto <same make and model as setup> <photo>", value="Add a photo to the car database", inline=False)
        embed1.add_field(name="carupdate <same make and model as setup>", value="Add info about your car to the database", inline=False)
        embed1.add_field(name="car <member/none>", value="Look up your own or someone else's car!", inline=False)
        embed1.add_field(name="rmcar <make and model>", value="Removes your car from the database", inline=False)
        embed1.add_field(name="STEP BY STEP INSTRUCTIONS", value="Step 1: run `carsetup <make and model> ", inline=False)

    @commands.command()
    async def psetup(self, ctx, name = None):    
        DB_PATH = "./data/db/database.db"

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()

        cur.execute(f"SELECT Name FROM profiles WHERE UserID = {ctx.message.author.id}")
        result = cur.fetchone()

        if result is None:
            sql = ("INSERT INTO profiles(UserID, Name) VALUES(?,?)")
            val = (ctx.message.author.id, model)
            cur.execute(sql, val)
            db.commit()
        cur.close()
        db.close()

    
    
def setup(bot):
    bot.add_cog(Profiles(bot))