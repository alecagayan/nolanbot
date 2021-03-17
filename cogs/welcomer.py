import discord
import asyncio
from discord.ext import commands


class Welcomer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):

        print('member 10 sec count now')

        await asyncio.sleep(10)

        print('10sec count over')
        role = discord.utils.get(member.guild.roles, name="YouTube Member")

        if role in member.roles:
            print('role found')
            channel = self.bot.get_channel(741398310228721844)
            guild = member.guild

            to_send = 'Welcome to the underground, {0.mention}.'.format(member, guild)
            await channel.send(to_send)
            await channel.send("Rule 1: welcome into the server, I hope you have a wonderful time in here! Please see <#731209804504367104> for the official server rules")
            await channel.send("Rule 2: if you would like to, please show us your car in <#733836074278846514>! All cars are welcome!")

    #sync def on_member_update(self, before, after):
#
#        print('update: ' + after.display_name)
#
#        print(before.roles)
#        print(after.roles)
        #if((any(role.name == 'Youtube Member' for role in after.roles) and any(role.name == 'Youtube Member: Donut Underground' for role in after.roles) and not any(role.name == 'Boost Creeps' for role in after.roles)) and len(after.roles) > len(before.roles)):
        #if((any(role.name == 'Youtube Member' for role in after.roles) and not any(role.name == 'Youtube Member: Donut Underground' for role in after.roles) or (any(role.name == 'Youtube Member: Donut Underground' for role in after.roles) and not any(role.name == 'Youtube Member' for role in after.roles))) and ((len(after.roles) > len(before.roles)) and not any(role.name == 'Boost Creeps' for role in after.roles)) ):
#        if((any(role.name == 'Youtube Member' for role in after.roles) and not any(role.name == 'Youtube Member' for role in before.roles)) and (len(after.roles) > len(before.roles))):
#            channel = self.bot.get_channel(741398310228721844)
#            guild = before.guild
#            print('member! ' + after.display_name)
#
#            to_send = 'Welcome to the underground, {0.mention}.'.format(before, guild)
#            await channel.send(to_send)

def setup(bot):
    bot.add_cog(Welcomer(bot))
