import discord
import asyncio
import json
import random
import urllib.request
import json
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def lyrics(self, ctx, *, title):
        response = await ctx.bot.srapi.get_lyrics(title)
        lyric = response.lyrics
        finallyric = (lyric[:1020] + '...') if len(lyric) > 1020 else lyric

        embedColor = 0xFFD414
        embed = discord.Embed(title="Lyrics of " + response.title + " by " + response.author + ":", color=embedColor)
        embed.set_thumbnail(url=response.thumbnail)
        embed.add_field(name = response.title, value=finallyric, inline=True)
        embed.add_field(name = 'Full lyrics: ', value=response.link, inline=False)
        await ctx.send(embed = embed)


    @commands.command()
    @commands.guild_only()
    async def lyrics(self, ctx, *, title):

        data = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&id=UCL6JmiMXKoXS6bpP1D3bk8g&key=").read()
        subs = json.loads(data)["items"][0]["statistics"]["subscriberCount"]

        await ctx.send(name + " has " + "{:,d}".format(int(subs)) + " subscribers!🎉")

    @commands.guild_only()
    @commands.command(aliases=["servericon"])
    async def server_avatar(self, ctx):
        """ Get the current server icon """
        if not ctx.guild.icon:
            return await ctx.send("This server does not have a avatar...")
        await ctx.send(ctx.guild.icon_url_as(size=1024))

    @commands.command(aliases=['game', 'presence'])
    async def setgame(self, ctx, *args):
    #Sets the 'Playing' status.
        if(ctx.author.id == 401063536618373121):
            try:
                setgame = ' '.join(args)
                await client.change_presence(status=discord.Status.online, activity=discord.Game(setgame))
                await ctx.send(":ballot_box_with_check: Game name set to: `" + setgame + "`")
                print("Game set to: `" + setgame + "`")
            except Exception as e:
                print('erroreeee: ' + e)
            return
        else:
            await ctx.send(config.err_mesg_permission)

    @commands.command()
    async def hug(self, ctx, *, member: discord.Member = None):
        """Hug someone on the server <3"""
        try:
            if member is None:
                await ctx.channel.purge(limit=1)
                await ctx.send(ctx.message.author.mention + " has been hugged!")
                await ctx.send("https://gph.is/g/ajxG084")
            else:
                if member.id == ctx.message.author.id:
                    await ctx.channel.purge(limit=1)
                    await ctx.send(ctx.message.author.mention + " has hugged themself!")
                    await ctx.send("https://gph.is/g/ajxG084")
                else:
                    await ctx.channel.purge(limit=1)
                    await ctx.send(member.mention + " has been hugged by " + ctx.message.author.mention + "!")
                    await ctx.send("https://gph.is/g/ajxG084")

        except Exception as e:
            print('erroreeee: ' + e)
        return

def setup(bot):
    bot.add_cog(Fun(bot))

