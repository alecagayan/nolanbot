import discord
import asyncio
import json
import random
import urllib.request
import json
import sr_api
from discord.ext import commands

def date(target, clock=True):
    """ Clock format using datetime.strftime() """
    if not clock:
        return target.strftime("%d %B %Y")
    return target.strftime("%d %B %Y, %H:%M")

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.dm_only()
    async def sendinnewmembers(self, ctx, *, msg):
        if(ctx.author.id == 401063536618373121):
            channel = self.bot.get_channel(741398310228721844)
            await channel.send(msg)

    
    @commands.command()
    @commands.guild_only()
    async def vote(self, ctx, *, msg):
        """ Quick y/n poll """

        await ctx.message.add_reaction("👍")
        await ctx.message.add_reaction("👎")

    @commands.command()
    @commands.guild_only()
    async def joined(self, ctx, *, user: discord.Member = None):
        """ Check when a user joined the current server """
        user = user or ctx.author

        embed = discord.Embed(color=user.top_role.colour.value)
        embed.set_thumbnail(url=user.avatar_url)
        embed.description = f'**{user}** joined **{ctx.guild.name}**\n{date(user.joined_at)}'
        await ctx.send(embed=embed)


#    @commands.command()
#    @commands.guild_only()
#    async def lyrics(self, ctx, *, title):
#       response = await ctx.bot.srapi.get_lyrics(title)
#        lyric = response.lyrics
#        finallyric = (lyric[:1020] + '...') if len(lyric) > 1020 else lyric
#
#        embedColor = 0xFFD414
#        embed = discord.Embed(title="Lyrics of " + response.title + " by " + response.author + ":", color=embedColor)
#        embed.set_thumbnail(url=response.thumbnail)
#        embed.add_field(name = response.title, value=finallyric, inline=True)
#        embed.add_field(name = 'Full lyrics: ', value=response.link, inline=False)
#        await ctx.send(embed = embed)

    @commands.command()
    @commands.guild_only()
    async def lyrics(self, ctx, *, title):
        srapi = sr_api.Client()
        response = await srapi.get_lyrics(title)
        lyric = response.lyrics
        finallyric = (lyric[:1020] + '...') if len(lyric) > 1020 else lyric

        embedColor = random.randint(0, 0xffffff)
        embed = discord.Embed(title="Lyrics of " + response.title + " by " + response.author + ":", color=embedColor)
        embed.set_thumbnail(url=response.thumbnail)
        embed.add_field(name = response.title, value=finallyric, inline=True)
        embed.add_field(name = 'Full lyrics: ', value=response.link, inline=False)
        await ctx.send(embed = embed)

    @commands.guild_only()
    @commands.command(aliases=["servericon"])
    async def server_avatar(self, ctx):
        """ Get the current server icon """
        if not ctx.guild.icon:
            return await ctx.send("This server does not have a avatar...")
        await ctx.send(ctx.guild.icon_url_as(size=1024))

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

