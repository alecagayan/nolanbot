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

            to_send = 'Welcome to the underground, {0.mention}!'.format(member)
            await channel.send(to_send)

def setup(bot):
    bot.add_cog(Welcomer(bot))
