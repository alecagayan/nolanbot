import discord
import asyncio
import json
import datetime
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embedColor = 0xFFD414
        prefix = '!'
        message = await ctx.send("Select a page by reacting below!")
        # getting the message object for editing and reacting

        await message.add_reaction("1️⃣")
        await message.add_reaction("2️⃣")
        await message.add_reaction("3️⃣")
        await message.add_reaction("4️⃣")
        await message.add_reaction("5️⃣")


        embed1 = discord.Embed(title="Help Page 1/5", description="Need help? Look below", color=embedColor)
        embed1.add_field(name="Support server", value="[Invite link](https://discord.gg/MJejP9q)")
        embed1.add_field(name=prefix + "time", value="Reads the time in EST", inline=False)
        embed1.add_field(name=prefix + "math <x y z>", value="Gives the operation of **Y** and **Z** using the **X** operation.", inline=False)
        embed1.add_field(name=prefix + "covid <state/county> <name>", value="Gives coronavirus statistics", inline=False)
        embed1.add_field(name=prefix + "github", value="Gives the link to bot code", inline=False)
        embed1.add_field(name=prefix + "invite", value="Sends the bot invite", inline=False)
        embed1.add_field(name=prefix + "roll", value='Rolls a die', inline=False)
        embed1.add_field(name=prefix + "compliment", value="Compliments a user you tag. If nobody is tagged, a compliment will be printed", inline=False)
        embed1.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time

        embed2 = discord.Embed(title="Help Page 2/5", description="Need help? Look below!", color=embedColor)
        embed2.add_field(name="Support server", value="[Invite link](https://discord.gg/MJejP9q)")
        embed2.add_field(name=prefix + "insult", value="Insults a user you tag. If nobody is tagged, an insult will be printed", inline=False)
        embed2.add_field(name=prefix + "uptime", value="Shows the uptime of the bot", inline=False)
        embed2.add_field(name=prefix + "xkcd", value="Random XKCD comic", inline=False)
        embed2.add_field(name=prefix + "server", value="Gives server info", inline=False)
        embed2.add_field(name=prefix + "ping", value="Pings the bot", inline=False)
        embed2.add_field(name=prefix + "credit", value='Who made alcebot? Time to find out!', inline=False)
        embed2.add_field(name=prefix + "hug", value="Hug anyone in the server!", inline=False)
        embed2.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time

        embed3 = discord.Embed(title="Help Page 3/5", description="Need help? Look below", color=embedColor)
        embed3.add_field(name="Support server", value="[Invite link](https://discord.gg/MJejP9q)")
        embed3.add_field(name=prefix + "premium", value="You already have premium!", inline=False)
        embed3.add_field(name=prefix + "suggestion <suggestion>", value="Suggest a new feature or bug fix", inline=False)
        embed3.add_field(name=prefix + "weather <zip code> <c or f>", value="Get the weather at your location", inline=False)
        embed3.add_field(name=prefix + "info", value="Gives basic bot info", inline=False)
        embed3.add_field(name=prefix + "purge <num of msgs>", value="Purge a certain number of messages", inline=False)
        embed3.add_field(name=prefix + "netdiskcpu", value='Get info about the bot computer (owner only)', inline=False)
        embed3.add_field(name=prefix + "fancify <text>", value="Makes text 𝓕𝓐𝓝𝓒𝓨", inline=False)
        embed3.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time

        embed4 = discord.Embed(title="Help Page 4/5", description="Need help? Look below", color=embedColor)
        embed4.add_field(name="Support server", value="[Invite link](https://discord.gg/MJejP9q)")
        embed4.add_field(name=prefix + "botplatform", value="Gives a little info about the platform the bot runs on", inline=False)
        embed4.add_field(name=prefix + "getbans", value="Shows a list of banned users", inline=False)
        embed4.add_field(name=prefix + "userinfo", value="Gives info on a user", inline=False)
        embed4.add_field(name=prefix + "christmas", value="Christmas countdown!", inline=False)
        embed4.add_field(name=prefix + "newyear", value="New Year countdown!", inline=False)
        embed4.add_field(name=prefix + "ban", value='Bans the tagged user', inline=False)
        embed4.add_field(name=prefix + "unban", value="Unbans the tagged user", inline=False)
        embed4.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time

        embed5 = discord.Embed(title="Help Page 5/5", description="Need help? Look below", color=embedColor)
        embed5.add_field(name="Support server", value="[Invite link](https://discord.gg/MJejP9q)")
        embed5.add_field(name=prefix + "prefix <prefix>", value="Changes the bot prefix", inline=False)
        embed5.add_field(name=prefix + "enlarge <user>", value="Enlarge a user's profile photo", inline=False)
        embed5.add_field(name=prefix + "servericon", value="Shows the server's icon", inline=False)
        embed5.add_field(name=prefix + "base64 <encode | decode>", value="Encodes or decodes base64", inline=False)
        embed5.add_field(name=prefix + "lyrics <song>", value="Gets song lyrics", inline=False)
        embed5.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]

        while True:
            try:
                reaction, user = await self.ctx.wait_for("reaction_add", timeout=60, check=check)
                # waiting for a reaction to be added - times out after x seconds, 60 in this
                # example

                if str(reaction.emoji) == "1️⃣":
                    await message.edit(embed=embed1)
                    await message.remove_reaction(reaction, user)
                elif str(reaction.emoji) == "2️⃣":
                    await message.edit(embed=embed2)
                    await message.remove_reaction(reaction, user)
                elif str(reaction.emoji) == "3️⃣":
                    await message.edit(embed=embed3)
                    await message.remove_reaction(reaction, user)
                elif str(reaction.emoji) == "4️⃣":
                    await message.edit(embed=embed4)
                    await message.remove_reaction(reaction, user)
                elif str(reaction.emoji) == "5️⃣":
                    await message.edit(embed=embed5)
                    await message.remove_reaction(reaction, user)
                else:
                    await message.remove_reaction(reaction, user)
                    # removes reactions if the user tries to go forward on the last page or
                    # backwards on the first page
            except asyncio.TimeoutError:
                await message.delete()
                break

def setup(bot):
    bot.add_cog(Help(bot))