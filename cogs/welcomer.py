import discord
import asyncio
from discord.ext import commands


class Welcomer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):

        print('member')

        await asyncio.sleep(2)

        role = discord.utils.get(member.guild.roles, name="YouTube Member")

        if role in member.roles:
            print('role found')
            channel = self.bot.get_channel(741398310228721844)

            to_send = '**Welcome to the underground, {0.mention}!**'.format(member)

            await channel.send("Please read the <#731209804504367104> before continuing. <#788857573230772294> is a great resource if you have any questions. Otherwise, all mods have pink names and would be happy to help you out!\n\nPosting your car to <#733836074278846514> or your animal friend to <#734487049364832350> would make for a great introduction! If you’d like to add them to our database, head over to <#748994641721950288> and type `!dbhelp` to get started\n\nEnjoy your stay, and remember – be kind!")
            await channel.send(to_send)


def setup(bot):
    bot.add_cog(Welcomer(bot))
