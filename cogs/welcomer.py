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

            to_send = 'Welcome to the underground, {0.mention}.'.format(member)
            await channel.send(to_send)
            await channel.send("Rule 1: welcome into the server, I hope you have a wonderful time in here! Please see <#731209804504367104> for the official server rules\nRule 2: if you would like to, please show us your car in <#733836074278846514>! All cars are welcome!")
            await channel.send("Rule 3: please show us your pets! You can send pictures of your wonderful animal friends in <#734487049364832350>! p.s. I would die for them\nRule 4: Make sure to head over to <#748994641721950288> and use the **!dbhelp** command to add your car and pet to the Underground database!\n-DogeLord1998")

def setup(bot):
    bot.add_cog(Welcomer(bot))
