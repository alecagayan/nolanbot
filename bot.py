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

#@client.event
#async def on_member_join(member):
#    ment = member.mention
#    channel = client.get_channel(617877897096724509)
#    await channel.send(f"{ment} has joined the server.")
#    print(f"{member} has joined the server.")


@client.command()
async def die(ctx):
    if(ctx.author.id == 401063536618373121):
        await ctx.send("Drinking bleach.....")
        await client.close()
    else:
        await ctx.send(config.err_mesg_permission)

@client.command()
async def debug(ctx):
    await ctx.send(str(ctx.channel.id))

#prints invite
@client.command()
async def invite(ctx):
    await ctx.send("https://discord.com/oauth2/authorize?client_id=806589564448931910&scope=bot&permissions=8")

@client.command()
async def ping(ctx):
    """
    Pings the bot.
    """
    joke = random.choice(["NO FEAR", "MO INTERNET BABEH", "fire it up"])
    ping_msg = await ctx.send("Pinging Server...")
    await ping_msg.edit(content=joke + f" // ***{client.latency*1000:.0f}ms***")

@client.command()
async def hug(ctx, *, member: discord.Member = None):
    """Hug someone on the server <3"""
    try:
        if member is None:
            await ctx.channel.purge(limit=1)
            await ctx.send(ctx.message.author.mention + " has been hugged!")
            await ctx.send("https://gph.is/g/ajxG084")
        else:
            if member.id == ctx.message.author.id:
                await ctx.channel.purge(limit=1)
                await ctx.send(ctx.message.author.mention + " has hugged themself!")
                await ctx.send("https://gph.is/g/ajxG084")
            else:
                await ctx.channel.purge(limit=1)
                await ctx.send(member.mention + " has been hugged by " + ctx.message.author.mention + "!")
                await ctx.send("https://gph.is/g/ajxG084")

    except Exception as e:
        print('erroreeee: ' + e)
    return

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


    if(type == "county"):

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
    embedColor = random.randint(0, 0xffffff)

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

client.run(config.bbtoken)

