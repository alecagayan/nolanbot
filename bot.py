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

    @commands.command(aliases=['game', 'presence'])
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
    joke = random.choice(["NO FEAR", "MO INTERNET BABEH", "fire it up"])
    ping_msg = await ctx.send("Pinging Server...")
    await ping_msg.edit(content=joke + f" // ***{client.latency*1000:.0f}ms***")

#@client.command()
#async def covid(ctx, type = None, *, location = None):
#
#    await ctx.send('⚠️ `Please wait, this may take a while`')
#
#    if(type == "state"):
#
#        if (not os.path.exists(filename_state) or file_age_in_seconds(filename_state) > 3600):
#            urllib.request.urlretrieve("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv", filename_state)
#        location = location.title()
#        df = pd.read_csv(filename_state)
#        df_state = df[ df['state'] == location ]
#        fig = px.line(df_state, x = 'date', y = ['cases', 'deaths'], title='Cases and Deaths in ' + location)
#        fig.write_image(state_graph)
#        await ctx.send(file=discord.File(state_graph))
#
#
#    elif(type == "county"):
#
#        if (not os.path.exists(filename_county) or file_age_in_seconds(filename_county) > 3600):
#            urllib.request.urlretrieve("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv", filename_county)
#        location = location.title()
#        df = pd.read_csv(filename_county)
#        df_county = df[ df['county'] == location ]
#        fig = px.line(df_county, x = 'date', y = ['cases', 'deaths'], title='Cases and Deaths in ' + location)
#        fig.write_image(county_graph)
#        await ctx.send(file=discord.File(county_graph))
#
#    else:
#
#        if (not os.path.exists(filename_state) or file_age_in_seconds(filename_state) > 3600):
#            urllib.request.urlretrieve("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv", filename_state)
#        df = pd.read_csv(filename_county)
#        fig = px.pie(df, values='cases', names='state', color_discrete_sequence=px.colors.sequential.RdBu)
#        fig.update_traces(textposition='inside', textinfo='percent+label')
#        fig.write_image('plot-nation.png')
#        await ctx.send(file=discord.File(us_graph))

#@client.command()
#async def weather(ctx, a, t = None):
#    comma = ','
#    mgr = owm.weather_manager()
#
#    if comma in a:
#        observation = mgr.weather_at_place(a)
#    else:
#        observation = mgr.weather_at_zip_code(a, 'US')
#
#    weather = observation.weather
#    embedColor = 0xFFD414
#
#    if(t == 'f'):
#        cf = 'fahrenheit'
#        label = ' F'
#    elif(t == 'fahrenheit'):
#        cf = 'fahrenheit'
#        label = ' F'
#    elif(t == 'celsius'):
#        cf = 'celsius'
#        label = ' C'
#    else:
#        cf = 'celsius'
#        label = ' C'
#
#    embed = discord.Embed(title="Weather in " + a + " right now:", color=embedColor) #embed title with zip
#    embed.add_field(name="Temperature :thermometer:", value=str(weather.temperature(cf)['temp']) + label, inline=True) #temperature
#    embed.add_field(name="Feels like :snowflake:", value=str(weather.temperature(cf)['feels_like']) + label, inline=True) #temperature
#    embed.add_field(name="Conditions :white_sun_rain_cloud:", value=weather.detailed_status, inline=True) #conditions header with emoji conditions
#    embed.add_field(name="Wind Speed :wind_blowing_face:", value=str(round(weather.wind('miles_hour')['speed'], 1)) + ' mph', inline=True) #wind speed
#    embed.add_field(name="Wind Direction :dash:", value=str(round(weather.wind('miles_hour')['deg'], 1)) + '°', inline=True) #wind speed
#    embed.add_field(name="Humidity :droplet:", value=str(weather.humidity) + '%', inline=True) #humidity
#    embed.add_field(name="Visibility :eye:", value=str(round(weather.visibility_distance/1609.344, 1)) + ' miles', inline=True) #visibility
#    embed.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time
#    await ctx.send(embed=embed)


client.run(config.bbtoken)

