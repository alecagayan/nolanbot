import typing
import discord

import sqlite3
from sqlite3 import connect

from discord.ext import commands

DB_PATH = "./data/db/roles.db"


#reaction roles cog
class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    db = connect(DB_PATH, check_same_thread=False)
    cur = db.cursor()
    cur.execute('''
                CREATE TABLE IF NOT EXISTS roles (
                MessageID integer,
                Emoji text,
                RoleID integer
                );''')
    cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                UserID integer,
                BannedRoleID integer
                );''')
    db.commit()
    cur.close()
    db.close()


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        #get info from db based on msg
        msg = int(payload.message_id)

        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()
        cur.execute(f"SELECT * FROM roles WHERE MessageID = {msg}")
        fetch = cur.fetchall()

        if len(fetch) != 0:

            for row in fetch:
                if row[1] == str(payload.emoji):
                    role = discord.utils.get(payload.member.guild.roles, id=int(row[2]))
                    #check if user has been banned from this role
                    cur.execute(f"SELECT * FROM users WHERE UserID = {payload.user_id} AND BannedRoleID = {row[2]}")
                    fetch = cur.fetchall()
                    if len(fetch) == 0:
                        await payload.member.add_roles(role)
                    
                    break


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
            
            #get info from db based on msg
            msg = int(payload.message_id)
            member = self.bot.get_guild(payload.guild_id).get_member(payload.user_id)
    
            db = connect(DB_PATH, check_same_thread=False)
            cur = db.cursor()
            cur.execute(f"SELECT * FROM roles WHERE MessageID = {msg}")
            fetch = cur.fetchall()
    
            if len(fetch) != 0:
    
                for row in fetch:
                    if row[1] == str(payload.emoji):
                        role = discord.utils.get(member.guild.roles, id=int(row[2]))
                        await member.remove_roles(role)
                        break

    
    @commands.group(name="rr", invoke_without_command=True)
    async def rr(self, ctx):

        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid subcommand passed...')

    @rr.command(name="add")
    async def rr_add(self, ctx, msg: int, emoji: str, *, roleName: str):
        """Adds a reaction role to a message"""

        #get the message
        await ctx.send(f"Getting message {msg}...")
        #get channel with id 
        channel = self.bot.get_channel(819286169200230412)
        msg = await channel.fetch_message(msg)

        #get the role
        role = discord.utils.get(ctx.guild.roles, name=roleName)

        #add the reaction role
        await msg.add_reaction(emoji)

        #add the reaction role to the database
        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()
        cur.execute(f"INSERT INTO roles VALUES(?, ?, ?)", (msg.id, emoji, role.id))
        db.commit()
        cur.close()
        db.close()

        await ctx.send(f"Added reaction role {emoji} to message {msg.id}")

    @rr.command(name="remove")
    async def rr_remove(self, ctx, msg: int, emoji: str):
        """Removes a reaction role from a message"""

        #get the message
        msg = await ctx.fetch_message(msg)

        #remove the reaction role
        await msg.remove_reaction(emoji, ctx.author)

        #remove the reaction role from the database
        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()
        cur.execute(f"DELETE FROM roles WHERE MessageID = {msg.id} AND Emoji = '{emoji}'")
        db.commit()
        cur.close()
        db.close()

        await ctx.send(f"Removed reaction role {emoji} from message {msg.id}")

    @rr.command(name="list")
    async def rr_list(self, ctx, msg: int):
        """Lists all reaction roles for a message"""

        #get the message
        msg = await ctx.fetch_message(msg)

        #get the reaction roles
        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()
        cur.execute(f"SELECT * FROM roles WHERE MessageID = {msg.id}")
        fetch = cur.fetchall()
        cur.close()
        db.close()

        if len(fetch) == 0:
            await ctx.send("No reaction roles found for this message")
        else:
            embed = discord.Embed(title="Reaction Roles", description="Reaction Roles for message {}".format(msg.id), color=0x00ff00)
            for row in fetch:
                embed.add_field(name=row[1], value=row[2], inline=False)
            await ctx.send(embed=embed)

    @rr.command(name="eject")
    async def rr_eject(self, ctx, user: discord.Member, *, role: str):
        """Ejects a user from a reaction role"""

        #get the role
        role = discord.utils.get(ctx.guild.roles, name=role)

        #remove the role from the user
        await user.remove_roles(role)

        #check if user is in users table with banned role
        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()
        cur.execute(f"SELECT * FROM users WHERE UserID = {user.id} AND BannedRoleID = {role.id}")
        fetch = cur.fetchall()

        #if user is in users table with banned role, say they are ejected
        if len(fetch) != 0:
            await ctx.send(f"{user.mention} is already ejected from {role.name}")
        else:
            #if user is not in users table with banned role, add them to the table
            cur.execute(f"INSERT INTO users VALUES({user.id}, {role.id})")
            db.commit()
            cur.close()
            db.close()

            await ctx.send(f"{user.mention} is now ejected from {role.name}")

    @rr.command(name="uneject")
    async def rr_uneject(self, ctx, user: discord.Member, *, role: str):
        """Unejects a user from a reaction role"""

        #get the role
        role = discord.utils.get(ctx.guild.roles, name=role)

        #remove the role from the user
        await user.remove_roles(role)

        #check if user is in users table with banned role
        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()
        cur.execute(f"SELECT * FROM users WHERE UserID = {user.id} AND BannedRoleID = {role.id}")
        fetch = cur.fetchall()

        #if user is in users table with banned role, say they are ejected
        if len(fetch) != 0:
            #remove user from users table
            cur.execute(f"DELETE FROM users WHERE UserID = {user.id} AND BannedRoleID = {role.id}")
            db.commit()
            cur.close()
            db.close()

            await ctx.send(f"{user.mention} is now un-ejected from {role.name}")
        else:
            await ctx.send(f"{user.mention} is not ejected from {role.name}")




def setup(bot):
    bot.add_cog(Reactions(bot))