import discord
import datetime
from discord.ext import commands

class Helpme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def helpme(self, ctx, tag = None):
        
        if(tag == 'sticker'):
            await ctx.send('Check out <#788841099325079622> for all your sticker related questions!')
        elif tag == 'order':
            await ctx.send("Hey there, looks like you're having a problem with your order.\nThe first step you should take is to go ahead and **take a look at the <#788857573230772294> channel**. The Donut team is not directly associated with merch, so **the best way to get ahold of the merch team would be to email `shop@donut.media`!**")
        elif tag == 'server':
            await ctx.send("THIS... is the Donut Underground discord server, and today I'm gonna show you all around it. We're gonna look at the wonderful quirks and features, then I'm gonna take you out for a tour, and then I'm gonna give it a Doug Score. An adventure awaits you, head to <#731210410614849586> to learn more!")
        elif tag == 'perks':
            await ctx.send("As a Donut Underground member, many perks await you. You get to chat in this server along with getting behind the scenes videos, a merch discount, loyalty badges and emojis, and an exclusive sticker mailed every 3 months!")
        elif tag == None:
                embed=discord.Embed(title='Available Tags', description='The tags below are available to use with the !helpme command!', color=0xf1c40f)
                embed.set_thumbnail(url=ctx.guild.icon_url)
                embed.add_field(name='sticker', value='Get info about your sticker order', inline=True)
                embed.add_field(name='order', value='Merch order information here', inline=True)
                embed.add_field(name='server', value='Server info', inline=True)
                embed.add_field(name='perks', value='What perks do you get as a member? Find out here', inline=True)
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Helpme(bot))