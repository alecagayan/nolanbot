import discord
import asyncio
import json
import datetime
from datetime import date
from discord.ext import commands, tasks

bd_names = {}
users_to_celebrate = []


def add_person(person_name, date):
    with open('birthdays.json', 'r') as f:
        bd_names = json.load(f)

    print(bd_names)
    today = datetime.datetime.today()
    print(today.day)

    bd_names[person_name] = date
    with open('birthdays.json', 'w') as json_file:
        json.dump(bd_names, json_file, indent=4)

time_for_thing_to_happen = datetime.time(hour=0)  # 0000UTC - suck it PST people

#async def timedtask():
#    while True:
#        now = datetime.datetime.utcnow()
#        date = now.date()
#        if now.time() > time_for_thing_to_happen:
#            date = now.date() + datetime.timedelta(days=1)
#        then = datetime.datetime.combine(date, time_for_thing_to_happen)
#        await discord.utils.sleep_until(then)
#        birthdaycheck()
#errors in tasks raise silently normally so lets make them speak up
#def exception_catching_callback(task):
#    if task.exception():
#        task.print_stack()
class Birthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
#    task = asyncio.create_task(timedtask())
#    task.add_done_callback(exception_catching_callback)

    @tasks.loop(hours=24)
    async def birthdaycheck(self):
        with open('birthdays.json', 'r') as f:
            bd_names = json.load(f)
        today = datetime.datetime.today()
        day = today.day
        month = today.month

        if todaysdate == None:
            todaysdate = str(today.month) + '/' + str(today.day)

        name = str(ctx.author.id)

        print(bd_names)
        print(todaysdate)

        if name in bd_names:
            for name in bd_names:
                if bd_names[name] == todaysdate:
                    print(name, "'s birthday is ", bd_names[name])
                    #channel = self.bot.get_channel(819296626103025705)
                    msg = await channel.send("Happy birthday <@" + name + ">!")
                    await msg.add_reaction('🎂')
                    await msg.add_reaction('🎉')
                    await msg.add_reaction('🥳')

    birthdaycheck.start()

    @commands.command()
    async def birthday(self, ctx, *, bday):

        user_input = ctx.author.id
        date_input = bday

        add_person(user_input, date_input)

        await ctx.message.add_reaction("🎂")

    @commands.command()
    async def birthdaystoday(self, ctx, todaysdate = None):
        with open('birthdays.json', 'r') as f:
            bd_names = json.load(f)
        today = datetime.datetime.today()
        day = today.day
        month = today.month

        if todaysdate == None:
            todaysdate = str(today.month) + '/' + str(today.day)

        name = str(ctx.author.id)

        print(bd_names)
        print(todaysdate)

        if name in bd_names:
            for name in bd_names:
                if bd_names[name] == todaysdate:
                    print(name, "'s birthday is ", bd_names[name])
                    #channel = self.bot.get_channel(819296626103025705)
                    msg = await ctx.send("Happy birthday <@" + name + ">!")
                    await msg.add_reaction('🎂')
                    await msg.add_reaction('🎉')
                    await msg.add_reaction('🥳')
    
    @commands.command()
    async def allbirthdays(self, ctx):
        with open('birthdays.json', 'r') as f:
            bd_names = json.load(f)

        for name in bd_names:
            member = ctx.guild.get_member(name)
            await ctx.send(str(member.nick) + str(bd_names[name]))




def setup(bot):
    bot.add_cog(Birthday(bot))

