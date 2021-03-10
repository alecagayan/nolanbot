import discord
import config
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
import plotly.express as px
from discord.ext.commands import Bot
from discord.ext import commands

filename_state = os.path.join(config.botdir, "us-states.csv")
filename_county = os.path.join(config.botdir, "us-counties.csv")
county_graph = os.path.join(config.botdir, 'plot-county.png')
state_graph = os.path.join(config.botdir, 'plot-state.png')
us_graph = os.path.join(config.botdir, 'plot-nation.png')

owm = pyowm.OWM(config.owm_key)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
client = Bot(description=config.des, command_prefix=config.pref, intents=intents)

newUserMessage = 'testing!!!'

def file_age_in_seconds(pathname):
    return os.path.getmtime(pathname)

client.load_extension("cogs.welcomer")
client.remove_command('help')
#client.load_extension("cogs.help")
client.load_extension("cogs.fun")

# Start bot and print status to console

@client.event
async def on_ready():
    print("Bot online!\n")
    print("Discord.py API version:", discord.__version__)
    print("Python version:", platform.python_version())
    print("Running on:", platform.system(), platform.release(), "(" + os.name + ")")
    print("Name : {}".format(client.user.name))
    print("Client ID : {}".format(client.user.id))
    print("Currently active on " + str(len(client.guilds)) + " server(s).\n")
    logger.info("Bot started successfully.")

    await client.change_presence(status=discord.Status.online, activity=discord.Game('hi nolan'))

@client.command()
async def die(ctx):
    if(ctx.author.id == 401063536618373121):
        await ctx.send("Drinking bleach.....")
        await client.close()
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
    joke = random.choice(["NO FEAR", "MO INTERNET BABEH", "fire it up"])
    ping_msg = await ctx.send("Pinging Server...")
    await ping_msg.edit(content=joke + f" // ***{client.latency*1000:.0f}ms***")

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
async def weather(ctx, a, t = None):
    comma = ','
    mgr = owm.weather_manager()

    if comma in a:
        observation = mgr.weather_at_place(a)
    else:
        observation = mgr.weather_at_zip_code(a, 'US')

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

    embed = discord.Embed(title="Weather in " + a + " right now:", color=embedColor) #embed title with zip
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
async def help(ctx):

    embedColor = random.randint(0, 0xffffff)

    message = await ctx.send("Select a page by reacting below!")
    # getting the message object for editing and reacting

    await message.add_reaction("1️⃣")
    await message.add_reaction("2️⃣")
    await message.add_reaction("3️⃣")
    await message.add_reaction("4️⃣")
    await message.add_reaction("5️⃣")

    with open('prefixes.json', 'r') as f:
        prefixes=json.load(f)
        prefix = prefixes[str(ctx.guild.id)]

    embed1 = discord.Embed(title="Help Page 1/5", description="Need help? Look below", color=embedColor)
    embed1.add_field(name=prefix + "time", value="Reads the time in EST", inline=False)
    embed1.add_field(name=prefix + "math <x y z>", value="Gives the operation of **Y** and **Z** using the **X** operation.", inline=False)
    embed1.add_field(name=prefix + "covid <state/county> <name>", value="Gives coronavirus statistics", inline=False)
    embed1.add_field(name=prefix + "github", value="Gives the link to bot code", inline=False)
    embed1.add_field(name=prefix + "invite", value="Sends the bot invite", inline=False)
    embed1.add_field(name=prefix + "roll", value='Rolls a die', inline=False)
    embed1.add_field(name=prefix + "compliment", value="Compliments a user you tag. If nobody is tagged, a compliment will be printed", inline=False)
    embed1.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time

    embed2 = discord.Embed(title="Help Page 2/5", description="Need help? Look below!", color=embedColor)
    embed2.add_field(name="Support server", value="[Invite link](https://discord.gg/MJejP9q)")
    embed2.add_field(name=prefix + "insult", value="Insults a user you tag. If nobody is tagged, an insult will be printed", inline=False)
    embed2.add_field(name=prefix + "uptime", value="Shows the uptime of the bot", inline=False)
    embed2.add_field(name=prefix + "xkcd", value="Random XKCD comic", inline=False)
    embed2.add_field(name=prefix + "server", value="Gives server info", inline=False)
    embed2.add_field(name=prefix + "ping", value="Pings the bot", inline=False)
    embed2.add_field(name=prefix + "credit", value='Who made alcebot? Time to find out!', inline=False)
    embed2.add_field(name=prefix + "hug", value="Hug anyone in the server!", inline=False)
    embed2.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time

    embed3 = discord.Embed(title="Help Page 3/5", description="Need help? Look below", color=embedColor)
    embed3.add_field(name="Support server", value="[Invite link](https://discord.gg/MJejP9q)")
    embed3.add_field(name=prefix + "premium", value="You already have premium!", inline=False)
    embed3.add_field(name=prefix + "suggestion <suggestion>", value="Suggest a new feature or bug fix", inline=False)
    embed3.add_field(name=prefix + "weather <zip code> <c or f>", value="Get the weather at your location", inline=False)
    embed3.add_field(name=prefix + "info", value="Gives basic bot info", inline=False)
    embed3.add_field(name=prefix + "purge <num of msgs>", value="Purge a certain number of messages", inline=False)
    embed3.add_field(name=prefix + "netdiskcpu", value='Get info about the bot computer (owner only)', inline=False)
    embed3.add_field(name=prefix + "fancify <text>", value="Makes text 𝓕𝓐𝓝𝓒𝓨", inline=False)
    embed3.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time

    embed4 = discord.Embed(title="Help Page 4/5", description="Need help? Look below", color=embedColor)
    embed4.add_field(name="Support server", value="[Invite link](https://discord.gg/MJejP9q)")
    embed4.add_field(name=prefix + "botplatform", value="Gives a little info about the platform the bot runs on", inline=False)
    embed4.add_field(name=prefix + "getbans", value="Shows a list of banned users", inline=False)
    embed4.add_field(name=prefix + "userinfo", value="Gives info on a user", inline=False)
    embed4.add_field(name=prefix + "christmas", value="Christmas countdown!", inline=False)
    embed4.add_field(name=prefix + "newyear", value="New Year countdown!", inline=False)
    embed4.add_field(name=prefix + "ban", value='Bans the tagged user', inline=False)
    embed4.add_field(name=prefix + "unban", value="Unbans the tagged user", inline=False)
    embed4.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time

    embed5 = discord.Embed(title="Help Page 5/5", description="Need help? Look below", color=embedColor)
    embed5.add_field(name="Support server", value="[Invite link](https://discord.gg/MJejP9q)")
    embed5.add_field(name=prefix + "prefix <prefix>", value="Changes the bot prefix", inline=False)
    embed5.add_field(name=prefix + "enlarge <user>", value="Enlarge a user's profile photo", inline=False)
    embed5.add_field(name=prefix + "servericon", value="Shows the server's icon", inline=False)
    embed5.add_field(name=prefix + "base64 <encode | decode>", value="Encodes or decodes base64", inline=False)
    embed5.add_field(name=prefix + "lyrics <song>", value="Gets song lyrics", inline=False)
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

client.run(config.bbtoken)

