import discord
from discord.ext import commands


class Welcomer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_member_update(self, before, after):

        if(any(role.name == 'GiGØ' for role in after.roles) and not any(role.name == 'alce' for role in after.roles) and after.roles > before.roles):
            guild = before.guild
            print('member!')
            if guild.system_channel is not None:
                to_send = 'Welcome to the underground, {0.mention}.'.format(before, guild)
                await guild.system_channel.send(to_send)

def setup(bot):
    bot.add_cog(Welcomer(bot))
