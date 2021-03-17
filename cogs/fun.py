import discord
import asyncio
import json
import random
import urllib.request
import json
import sr_api
from discord.ext import commands
from discord.ext.commands import clean_content

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
    async def sendinserver(self, ctx, channelid, *, msg):
        if(ctx.author.id == 401063536618373121):
            print(channelid)
            channel = self.bot.get_channel(channelid)
            await channel.send(msg)

    
    @commands.command()
    @commands.guild_only()
    async def vote(self, ctx, *, msg):
        """ Quick y/n poll """

        await ctx.message.add_reaction("👍")
        await ctx.message.add_reaction("👎")

    @commands.command(aliases=['8ball']) # THANK YOU SO MUCH TO https://github.com/SpectrixDev
    async def eightball(self, ctx, *, _ballInput: clean_content):
        """extra generic just the way you like it"""
        choiceType = random.choice(["(Affirmative)", "(Non-committal)", "(Negative)"])
        if choiceType == "(Affirmative)":
            prediction = random.choice(["It is certain ", 
                                        "It is decidedly so ", 
                                        "Without a doubt ", 
                                        "Yes, definitely ", 
                                        "You may rely on it ", 
                                        "As I see it, yes ",
                                        "Most likely ", 
                                        "Outlook good ", 
                                        "Yes ", 
                                        "Signs point to yes "]) + ":8ball:"

            emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0x3be801, description=prediction))
        elif choiceType == "(Non-committal)":
            prediction = random.choice(["Reply hazy try again ", 
                                        "Ask again later ", 
                                        "Better not tell you now ", 
                                        "Cannot predict now ", 
                                        "Concentrate and ask again "]) + ":8ball:"
            emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0xff6600, description=prediction))
        elif choiceType == "(Negative)":
            prediction = random.choice(["Don't count on it ", 
                                        "My reply is no ", 
                                        "My sources say no ", 
                                        "Outlook not so good ", 
                                        "Very doubtful "]) + ":8ball:"
            emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0xE80303, description=prediction))
        emb.set_author(name='Magic 8 ball', icon_url='https://www.horoscope.com/images-US/games/game-magic-8-ball-no-text.png')
        await ctx.send(embed=emb)

    @commands.command()
    @commands.guild_only()
    async def joined(self, ctx, *, user: discord.Member = None):
        """ Check when a user joined the current server """
        user = user or ctx.author

        embed = discord.Embed(color=user.top_role.colour.value)
        embed.set_thumbnail(url=user.avatar_url)
        embed.description = f'**{user}** joined **{ctx.guild.name}**\n{date(user.joined_at)}'
        await ctx.send(embed=embed)

    @commands.command()
    async def reverse(self, ctx, *, s: clean_content):
        result = await commands.clean_content().convert(ctx, s[::-1])
        if len(result) <= 350:
            await ctx.send(f"{result}")
        else:
            try:
                await ctx.author.send(f"{result}")
                await ctx.send(f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**")
            except Exception:
                await ctx.send(f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**")

    @commands.command()
    async def mockme(self, ctx, member: discord.Member = None):

        insult = random.choice(["you oil-leaking shitbox",
                                "you're a few gears short of a 6 speed aren't you",
                                "you better watch your damn mouth before I take you to gapplebees"])
        if(member == None):
            await ctx.send(insult)
        else:
            await ctx.send(member.mention, insult)

    @commands.command()
    async def engineer(self, ctx):
        await ctx.send('https://tenor.com/view/engineer-yee-haw-dosido-square-dance-engineer-dancing-gif-15569822')

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
    async def hug(self, ctx, member: discord.Member = None, member2: discord.Member = None, member3: discord.Member = None):
        """Hug someone on the server <3"""
        try:
            if member is None:
                await ctx.send(ctx.message.author.mention + " has been hugged!")
                await ctx.send("https://gph.is/g/ajxG084")
            else:
                if member.id == ctx.message.author.id:
                    await ctx.send(ctx.message.author.mention + " has hugged themself!")
                    await ctx.send("https://gph.is/g/ajxG084")
                else:
                    await ctx.send(member.mention + " has been hugged by " + ctx.message.author.mention + "!")
                    await ctx.send("https://gph.is/g/ajxG084")

        except Exception as e:
            print('erroreeee: ' + e)
        return

def setup(bot):
    bot.add_cog(Fun(bot))

