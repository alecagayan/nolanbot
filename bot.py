import discord
import config
import psutil
import platform
import json
import os
import logging
import random
import pyowm
import datetime
import urllib
import urllib.request
import pandas as pd
import asyncio
import time
import wikipedia
import plotly.express as px
from discord.ext.commands import Bot
from discord.ext import commands
import sqlite3
from os.path import isfile
from sqlite3 import connect

filename_state = os.path.join(config.botdir, "us-states.csv")
filename_county = os.path.join(config.botdir, "us-counties.csv")
county_graph = os.path.join(config.botdir, 'plot-county.png')
state_graph = os.path.join(config.botdir, 'plot-state.png')
us_graph = os.path.join(config.botdir, 'plot-nation.png')

start_time = time.time()

owm = pyowm.OWM(config.owm_key)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
client = Bot(description=config.des, command_prefix=config.pref, intents=intents)

def file_age_in_seconds(pathname):
    return os.path.getmtime(pathname)
    
client.remove_command('help')
client.load_extension("cogs.welcomer")
client.load_extension("cogs.poll")
client.load_extension("cogs.birthday")
client.load_extension("cogs.helpme")
client.load_extension("cogs.cars")
client.load_extension("cogs.pets")
client.load_extension("cogs.games")
client.load_extension("cogs.profiles")
#client.load_extension("cogs.fun")
client.load_extension("cogs.xp")
client.load_extension("cogs.roles")
client.load_extension("cogs.custom")
client.load_extension("cogs.trivia")
client.load_extension("cogs.qa")

# Start bot and print status to console

@client.event
async def on_ready():

    DB_PATH = "./data/db/database.db"
    BUILD_PATH = "./data/db/build.sql"

    db = connect(DB_PATH, check_same_thread=False)
    cur = db.cursor()

    cur.execute('''
                CREATE TABLE IF NOT EXISTS cars (
                UserID integer, 
                Car text,
                Photo text,
                Color text,
                Year text,
                Miles text,
                Mods text,
                Extra1 text,
                Extra2 text,
                Extra3 text,
                Extra4 text,
                Extra5 text DEFAULT CURRENT_TIMESTAMP
                );''')

    cur.execute('''
                CREATE TABLE IF NOT EXISTS pets (
                UserID integer,
                Pet text,
                Photo text,
                Type text,
                Age text,
                Mods text,
                AsOf text DEFAULT CURRENT_TIMESTAMP
                );''')

    cur.execute('''
            CREATE TABLE IF NOT EXISTS profiles (
            UserID integer,
            Name text,
            Bio text,
            Pronouns text,
            Age text,
            Mods text,
            Extra1 text,
            Extra2 text,
            Extra3 text,
            Extra4 text,
            Extra5 text,
            AsOf text DEFAULT CURRENT_TIMESTAMP
            );''')
    db.commit()
    cur.close()
    db.close()

    print("Bot online!\n")
    print("Discord.py API version:", discord.__version__)
    print("Python version:", platform.python_version())
    print("Running on:", platform.system(), platform.release(), "(" + os.name + ")")
    print("Name : {}".format(client.user.name))
    print("Client ID : {}".format(client.user.id))
    print("Currently active on " + str(len(client.guilds)) + " server(s).\n")
    logger.info("Bot started successfully.")

    await client.change_presence(status=discord.Status.online, activity=discord.Game('with cars'))

@client.command()
async def die(ctx):
    if(ctx.author.id == 401063536618373121):
        await ctx.send("Drinking bleach.....")
        await client.close()
    else:
        await ctx.send(config.err_mesg_permission)

@client.command()
async def hello(ctx):
    def check(m):
        return m.author == ctx.author
    await ctx.send("Hello")
    msg = await client.wait_for('message', check=check)
    await ctx.send(f"You said {msg.content}. Hi again.")

@client.command(aliases=['github', 'git'])
async def commit(ctx):
    await ctx.send('https://github.com/oopsie1412/nolanbot')

@client.command(aliases=['game', 'presence'])
async def setgame(self, ctx, *args):
#Sets the 'Playing' status.
    if(ctx.author.id == 401063536618373121):
        try:
            setgame = ' '.join(args)
            await client.change_presence(status=discord.Status.online, activity=discord.Game(setgame))
            await ctx.send(":ballot_box_with_check: Game name set to: `" + setgame + "`")
            print("Game set to: `" + setgame + "`")
        except Exception as e:
            print('erroreeee: ' + e)
        return
    else:
        await ctx.send(config.err_mesg_permission)

#roll a die
@client.command()
async def roll(ctx):
    await ctx.send(config.die_url[random.randint(1,6)-1])

@client.command()
async def ping(ctx):
    """
    Pings the bot.
    """
    joke = random.choice(["NO FEAR", "MO INTERNET BABEH", "fire it up", "LIGHTNING"])
    ping_msg = await ctx.send("Pinging Server...")
    await ping_msg.edit(content=joke + f" // ***{client.latency*1000:.0f}ms***")

@client.command(pass_context=True, aliases=['serverinfo', 'guild', 'membercount'])
async def server(ctx):

    #prints server info
    roles = ctx.guild.roles
    embed = discord.Embed(color=0xf1c40f) #Golden
    role = discord.utils.get(ctx.guild.roles, name="YouTube Member")
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.add_field(name='Name', value=ctx.guild.name, inline=True)
    embed.add_field(name='ID', value=ctx.guild.id, inline=True)
    embed.add_field(name='Owner', value=ctx.guild.owner, inline=True)
    embed.add_field(name='Region', value=ctx.guild.region, inline=True)
    embed.add_field(name='Member Count', value=len(role.members), inline=True)
    embed.add_field(name='Creation', value=ctx.guild.created_at.strftime('%d.%m.%Y'), inline=True)
    embed.set_footer(text='Requested on ' + str(datetime.datetime.now()))
    await ctx.send(embed=embed)

@client.command()
async def wiki(ctx, *, query):
    newquery = wikipedia.suggest(query)
    if(newquery is not None):
        query = newquery

    embed=discord.Embed(title=wikipedia.page(query).title, url=wikipedia.page(query).url)
    embed.set_thumbnail(url=wikipedia.page(query).images[0])
    embed.add_field(name="Summary", value=wikipedia.summary(query, sentences=2), inline=False)
    await ctx.send(embed=embed)

@client.command()
async def code(ctx):
    await ctx.send("`DONUTUG10`")


@client.command(aliases=["fancy"])
async def fancify(ctx, *, text):
    """Makes text fancy!"""
    try:
        def strip_non_ascii(string):
            """Returns the string without non ASCII characters."""
            stripped = (c for c in string if 0 < ord(c) < 127)
            return ''.join(stripped)

        text = strip_non_ascii(text)
        if len(text.strip()) < 1:
            return await ctx.send(":x: ASCII characters only please!")
        output = ""
        for letter in text:
            if 65 <= ord(letter) <= 90:
                output += chr(ord(letter) + 119951)
            elif 97 <= ord(letter) <= 122:
                output += chr(ord(letter) + 119919)
            elif letter == " ":
                output += " "
        await ctx.send(output)

    except Exception as e:
        print(e)
    return

@client.command()
async def suggest(ctx, *, msg):
    user = client.get_user(401063536618373121)
    await user.send('**Suggestion:** ' + msg)

@client.command()
async def uptime(ctx):
    current_time = time.time()
    difference = int(round(current_time - start_time))
    text = str(datetime.timedelta(seconds=difference))
    embed = discord.Embed(colour=ctx.message.author.top_role.colour)
    embed.add_field(name="Uptime", value=text)
    embed.set_footer(text='Requested on ' + str(datetime.datetime.now()))

    await ctx.send(embed=embed)

@client.command()
async def stats(ctx):
    embedColor = random.randint(0, 0xffffff)
    embed = discord.Embed(title="Stats:", color=embedColor)

    embed.add_field(name="Net IO Counters", value=psutil.net_io_counters())
    embed.add_field(name="Disk IO Counters", value=psutil.disk_io_counters())
    embed.add_field(name="Disk Usage", value=psutil.disk_usage('/'))
    embed.add_field(name="CPU", value='Logical CPUs: ' +  str(psutil.cpu_count(logical=True))
                    + '\nCPU Frequency: ' +  str(psutil.cpu_freq(percpu=False))
                    + '\nCPU Load: ' + str(psutil.getloadavg())
                    + '\nCPU Temperature: ' + str(psutil.sensors_temperatures(fahrenheit=False)))
    embed.set_footer(text='Requested on ' + str(datetime.datetime.now()))

    await ctx.send(embed=embed)

@client.command()
async def perms(ctx):
    embed = discord.Embed(color=0xf1c40f) #Golden
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text='Requested on ' + str(datetime.datetime.now()))
    embed.add_field(name='Necessary Perms', value='Manage Messages\nView Channels\nSend Messages\nEmbed Links\nAttach Files\nAdd Reactions\nUse External Emoji\nManage Messages\nRead Message History', inline=False)
    embed.add_field(name='Future-Proof Perms', value='Connect\nSpeak', inline=False)
    embed.add_field(name='The simple way to go about this would be to give the bot admin:', value="But that's not very secure", inline=False)
    embed.set_footer(text='Requested on ' + str(datetime.datetime.now()))
    await ctx.send(embed=embed)

@client.command()
async def covid(ctx, type = None, *, location = None):

    await ctx.send('⚠️ `Please wait, this may take a while`')

    if(type == "state"):

        if (not os.path.exists(filename_state) or file_age_in_seconds(filename_state) > 3600):
            urllib.request.urlretrieve("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv", filename_state)
        location = location.title()
        df = pd.read_csv(filename_state)
        df_state = df[ df['state'] == location ]
        fig = px.line(df_state, x = 'date', y = ['cases', 'deaths'], title='Cases and Deaths in ' + location)
        fig.write_image(state_graph)
        await ctx.send(file=discord.File(state_graph))


    elif(type == "county"):

        if (not os.path.exists(filename_county) or file_age_in_seconds(filename_county) > 3600):
            urllib.request.urlretrieve("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv", filename_county)
        location = location.title()
        df = pd.read_csv(filename_county)
        df_county = df[ df['county'] == location ]
        fig = px.line(df_county, x = 'date', y = ['cases', 'deaths'], title='Cases and Deaths in ' + location)
        fig.write_image(county_graph)
        await ctx.send(file=discord.File(county_graph))

    else:

        if (not os.path.exists(filename_state) or file_age_in_seconds(filename_state) > 3600):
            urllib.request.urlretrieve("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv", filename_state)
        df = pd.read_csv(filename_county)
        fig = px.pie(df, values='cases', names='state', color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.write_image('plot-nation.png')
        await ctx.send(file=discord.File(us_graph))

@client.command()
async def weather(ctx, *a):
    t = a[len(a) - 1]
    if t in ['f', 'fahrenheit', 'c', 'celsius']:
        a = a[:len(a) - 1]

    location = ' '.join(map(str, a))
    comma = ','
    mgr = owm.weather_manager()

    if comma in location:
        observation = mgr.weather_at_place(location)
    else:
        observation = mgr.weather_at_zip_code(location, 'US')

    weather = observation.weather
    embedColor = 0xFFD414

    if(t == 'f'):
        cf = 'fahrenheit'
        label = ' F'
    elif(t == 'fahrenheit'):
        cf = 'fahrenheit'
        label = ' F'
    elif(t == 'celsius'):
        cf = 'celsius'
        label = ' C'
    else:
        cf = 'celsius'
        label = ' C'

    embed = discord.Embed(title="Weather in " + location + " right now:", color=embedColor) #embed title with zip
    embed.add_field(name="Temperature :thermometer:", value=str(weather.temperature(cf)['temp']) + label, inline=True) #temperature
    embed.add_field(name="Feels like :snowflake:", value=str(weather.temperature(cf)['feels_like']) + label, inline=True) #temperature
    embed.add_field(name="Conditions :white_sun_rain_cloud:", value=weather.detailed_status, inline=True) #conditions header with emoji conditions
    embed.add_field(name="Wind Speed :wind_blowing_face:", value=str(round(weather.wind('miles_hour')['speed'], 1)) + ' mph', inline=True) #wind speed
    embed.add_field(name="Wind Direction :dash:", value=str(round(weather.wind('miles_hour')['deg'], 1)) + '°', inline=True) #wind speed
    embed.add_field(name="Humidity :droplet:", value=str(weather.humidity) + '%', inline=True) #humidity
    embed.add_field(name="Visibility :eye:", value=str(round(weather.visibility_distance/1609.344, 1)) + ' miles', inline=True) #visibility
    embed.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time
    await ctx.send(embed=embed)

@client.command()
async def test(ctx):
    photo = ctx.message.attachments[0]
    await ctx.send(photo.url)

@client.command()
async def help(ctx):
    embedColor = 0xFFD414
    prefix = '!'
    message = await ctx.send("Select a page by reacting below!")
    # getting the message object for editing and reacting

    await message.add_reaction("1️⃣")
    await message.add_reaction("2️⃣")
    await message.add_reaction("3️⃣")
    await message.add_reaction("4️⃣")
    await message.add_reaction("5️⃣")


    embed1 = discord.Embed(title="Help Page 1/5", description="Need help? Look below", color=embedColor)
    embed1.add_field(name=prefix + "helpme <tag or empty for info>", value='Get DU related help and answers to your questions!', inline=False)
    embed1.add_field(name=prefix + "vote", value="Makes a quick yes/no poll", inline=False)
    embed1.add_field(name=prefix + "covid <state or county> <name>", value="Gives coronavirus statistics", inline=False)
    embed1.add_field(name=prefix + "lyrics <song name/artist>", value="Prints song lyrics", inline=False)
    embed1.add_field(name=prefix + "servericon", value="Returns the server icon", inline=False)
    embed1.add_field(name=prefix + "quickpoll", value="Creates a quick poll with multiple options", inline=False)
    embed1.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time

    embed2 = discord.Embed(title="Help Page 2/5", description="Need help? Look below!", color=embedColor)
    embed2.add_field(name=prefix + "weather <zip code> <c or f>", value="Get the weather at your location", inline=False)
    embed2.add_field(name=prefix + "uptime", value="Shows the uptime of the bot", inline=False)
    embed2.add_field(name=prefix + "server", value="Gives server info", inline=False)
    embed2.add_field(name=prefix + "fancify <text>", value="Makes text 𝓕𝓐𝓝𝓒𝓨", inline=False)
    embed2.add_field(name=prefix + "hug", value="Hug anyone in the server!", inline=False)
    embed2.add_field(name=prefix + "birthday <month/day>", value="Set your birthday!", inline=False)
    embed2.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time

    embed3 = discord.Embed(title="Help Page 3/5", description="Need help? Look below!", color=embedColor)
    embed3.add_field(name=prefix + "birthdaystoday", value="Announce today's birthdays!", inline=False)
    embed3.add_field(name=prefix + "roll", value='Rolls a die', inline=False)
    embed3.add_field(name=prefix + "joined <member>", value="Find out when a member joined the discord!", inline=False)
    embed3.add_field(name=prefix + "play <youtube url or video name>", value="Play a song in VC", inline=False)
    embed3.add_field(name=prefix + "pause", value="This one is pretty obvious", inline=False)
    embed3.add_field(name=prefix + "stop", value="Stops the song and leaves the voice channel", inline=False)
    embed3.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time

    embed4 = discord.Embed(title="Help Page 4/5", description="Need help? Look below!", color=embedColor)
    embed4.add_field(name=prefix + "np", value="Shows what is playing now", inline=False)
    embed4.add_field(name=prefix + "q", value='Shows a queue of upcoming songs', inline=False)
    embed4.add_field(name=prefix + "volume <1 - 100>", value="Set the volume of the bot in VC", inline=False)
    embed4.add_field(name=prefix + "suggest <suggestion>", value="PLEASE let me know how I can improve my work!", inline=False)
    embed4.add_field(name=prefix + "8ball <8ball query>", value="Outlook Good", inline=False)
    embed4.add_field(name=prefix + "reverse <text>", value="Reverses text: txet sesreveR", inline=False)
    embed4.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time

    embed5 = discord.Embed(title="Help Page 5/5", description="Need help? Look below!", color=embedColor)
    embed5.add_field(name=prefix + "mockme <optional user>", value="Shoots out a friendly insult", inline=False)
    embed5.add_field(name=prefix + "engineer", value='Shows a community-curated gif', inline=False)
    embed5.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time


    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]


    while True:
        try:
            reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)
            # waiting for a reaction to be added - times out after x seconds, 60 in this
            # example

            if str(reaction.emoji) == "1️⃣":
                await message.edit(embed=embed1)
                await message.remove_reaction(reaction, user)
            elif str(reaction.emoji) == "2️⃣":
                await message.edit(embed=embed2)
                await message.remove_reaction(reaction, user)
            elif str(reaction.emoji) == "3️⃣":
                await message.edit(embed=embed3)
                await message.remove_reaction(reaction, user)
            elif str(reaction.emoji) == "4️⃣":
                await message.edit(embed=embed4)
                await message.remove_reaction(reaction, user)
            elif str(reaction.emoji) == "5️⃣":
                await message.edit(embed=embed5)
                await message.remove_reaction(reaction, user)
            else:
                await message.remove_reaction(reaction, user)
                # removes reactions if the user tries to go forward on the last page or
                # backwards on the first page
        except asyncio.TimeoutError:
            await message.delete()
            break

@client.command()
async def dbhelp(ctx):
    embed1 = discord.Embed(title="Available Setup Commands (1/3)", description="Need database help? Look below", color=0xFFD414)
    embed1.add_field(name="carsetup <make and model>", value="Nolanbot will guide you through the setup process for a new car and will ask for information such as mileage, model year, color, and modifications", inline=False)
    embed1.add_field(name="carphoto <same make and model as setup> <photo>", value="Update your car's photo or add a photo for the first time. Make sure to attach a photo with the message", inline=False)
    embed1.add_field(name="carupdate <same make and model as setup>", value="Nolanbot will help you update information on your car such as mileage, model year, color, and modifications", inline=False)
    embed1.add_field(name="car <member/none>", value="Nolanbot will look up your car or someone else's car in the car database", inline=False)
    embed1.add_field(name="rmcar <make and model>", value="Nolanbot will remove your car from the database", inline=False)
    embed1.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time

    embed2 = discord.Embed(title="Available Setup Commands (2/3)", description="Need database help? Look below", color=0xFFD414)
    embed2.add_field(name="petsetup <name>", value="Nolanbot will guide you through the setup process for a new pet and will ask for information such as its age and pet type", inline=False)
    embed2.add_field(name="petphoto <same name as setup> <photo>", value="Update your pet's photo or add a photo for the first time. Make sure to attach a photo with the message", inline=False)
    embed2.add_field(name="petupdate <same name as setup>", value="Nolanbot will help you update information on your pet such as its age and pet type", inline=False)
    embed2.add_field(name="pet <member/none>", value="Nolanbot will look up your pet or someone else's pet in the pet database", inline=False)
    embed2.add_field(name="rmpet <name>", value="Nolanbot will remove your pet from the database", inline=False)
    embed2.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time

    embed3 = discord.Embed(title="Available Setup Commands (3/3)", description="Need database help? Look below", color=0xFFD414)
    embed3.add_field(name="psetup <name>", value="Nolanbot will guide you through the setup process for a new profile", inline=False)
    embed3.add_field(name="pbio", value="Add a bio to your profile. Keep this under 512 characters", inline=False)
    embed3.add_field(name="ppronouns", value="Add pronouns to your bio", inline=False)
    embed3.add_field(name="plink", value="Add a URL to your bio. Keep this under 256 characters", inline=False)
    embed3.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time
    message = await ctx.send(embed=embed1)

    await ctx.send("**Please read the wiki page for more information: https://wiki.nolanbot.xyz/wiki/Database_Commands**")
    # getting the message object for editing and reacting

    await message.add_reaction("1️⃣")
    await message.add_reaction("2️⃣")
    await message.add_reaction("3️⃣")


    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["1️⃣", "2️⃣", "3️⃣"]

    while True:
        try:
            reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)
            # waiting for a reaction to be added - times out after x seconds, 60 in this
            # example

            if str(reaction.emoji) == "1️⃣":
                await message.edit(embed=embed1)
                await message.remove_reaction(reaction, user)
            elif str(reaction.emoji) == "2️⃣":
                await message.edit(embed=embed2)
                await message.remove_reaction(reaction, user)
            elif str(reaction.emoji) == "3️⃣":
                await message.edit(embed=embed3)
                await message.remove_reaction(reaction, user)


        except asyncio.TimeoutError:
            break

client.run(config.bbtoken)
