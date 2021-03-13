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
            await ctx.send('Not sure what to put here, someone please help by committing to my repository at https://github.com/oopsie1412/donutbot')
        elif tag == 'membership':
            await ctx.send("Congrats, you're a member! You get to stay here and chat with the greatest car community in the world, right up until your membership expires.\nWhen your membership expires, you sadly won't be able to chat with the wonderful people here in the Donut Underground discord!")
        elif tag == 'donut':
            await ctx.send("Some info about donut, i think this is best left to someone who knows more than me haha")
        elif tag == 'server':
            await ctx.send("THIS... is the Donut Underground discord server, and today I'm gonna show you all around it. We're gonna look at the wonderful quirks and features, then I'm gonna take you out for a tour, and then I'm gonna give it a Doug Score. An adventure awaits you, head to <#731210410614849586> to learn more!")
        elif tag == 'perks':
            await ctx.send("As a Donut Underground member, many perks await you. You get to chat in this server along with getting behind the scenes videos, a merch discount, loyalty badges and emojis, and an exclusive sticker mailed every 3 months!")
        elif tag == None:
                embed=discord.Embed(title='Available Tags', description='The tags below are available to use with the !helpme command!', color=0xf1c40f)
                embed.set_thumbnail(url=ctx.guild.icon_url)
                embed.add_field(name='sticker', value='', inline=True)
                embed.add_field(name='order', value='', inline=True)
                embed.add_field(name='membership', value='', inline=True)
                embed.add_field(name='donut', value='', inline=True)
                embed.add_field(name='server', value='', inline=True)
                embed.add_field(name='perks', value='', inline=True)
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Helpme(bot))