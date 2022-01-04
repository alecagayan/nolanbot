import discord
import asyncio
import json
import random
import os
import io
import re
import csv

from discord.ext import commands
from discord.utils import get

class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def box(text: str, lang: str = "") -> str:
        return f"```{lang}\n{text}\n```"


    @commands.group()
    @commands.has_permissions(manage_messages=True)
    async def triviaset(self, ctx: commands.Context):  

        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid subcommand passed...')

    @triviaset.command(name="showsettings")
    async def triviaset_showsettings(self, ctx: commands.Context):
        #show the current settings
        with open('./data/json/triviasettings.json') as f:
            settings = json.load(f)

        guild_id = ctx.guild.id

        settings = settings[str(guild_id)]

        embed = discord.Embed(title="Trivia Settings", description="", color=0x00ff00)
        embed.add_field(name="Answer Time", value=str(settings["answer_time"]) + " seconds", inline=False)
        embed.add_field(name="Question Time", value=str(settings["question_time"]) + " seconds", inline=False)
        embed.add_field(name="Show Answer After Question", value=settings["show_answer_after_question"], inline=False)  
        embed.add_field(name="Show Leaderboard", value=settings["show_leaderboard"], inline=False)
        embed.add_field(name="Point Maximum", value=settings["point_maximum"], inline=False)
        embed.add_field(name="Point Minimum", value=settings["point_minimum"], inline=False)
        embed.set_footer(text=f"Use the command 'triviaset' to change these settings. {settings['hex']}")

        await ctx.send(embed=embed)

    @triviaset.command(name="setup")
    async def triviaset_setup(self, ctx: commands.Context):
        #set up the settings that the bot will use for this guild
        #if the guild has already been set up, do nothing
        #default settings:
        #answer_time: 10 seconds
        #question_time: 5 seconds
        #show_answer_after_question: True
        #show_leaderboard: True
        #point_minimum: 500
        #point_maximum: 1000

        with open('./data/json/triviasettings.json') as f:
            settings = json.load(f)
        if str(ctx.guild.id) in settings:
            await ctx.send("This guild has already been set up.")
            return

        #get the guild id
        guild_id = ctx.guild.id

        #create new dict for the guild
        settings[str(guild_id)] = {
            'answer_time': 10,
            'question_time': 5,
            'show_answer_after_question': True,
            'show_leaderboard': True,
            'point_minimum': 500,
            'point_maximum': 1000,
            'hex': '#' + ''.join([random.choice('0123456789ABCDEF') for x in range(6)])
        }

        #save the settings
        with open('./data/json/triviasettings.json', 'w') as f:
            json.dump(settings, f)

        #send message to guild with hex key
        await ctx.send(f"This guild has been set up. `{settings[str(guild_id)]['hex']}`")
    @triviaset.command(name="answertime")
    async def triviaset_answertime(self, ctx: commands.Context, time: int):
        #set the answer time for the current guild
        with open('./data/json/triviasettings.json') as f:
            settings = json.load(f)
        if str(ctx.guild.id) not in settings:
            await ctx.send("This guild has not been set up.")
            return

        #get the guild id
        guild_id = ctx.guild.id

        #set the answer time
        settings[str(guild_id)]['answer_time'] = time

        #save the settings
        with open('./data/json/triviasettings.json', 'w') as f:
            json.dump(settings, f)

        await ctx.send("The answer time has been set to " + str(time) + " seconds.")

    @triviaset.command(name="questiontime")
    async def triviaset_questiontime(self, ctx: commands.Context, time: int):
        #set the question time for the current guild
        with open('./data/json/triviasettings.json') as f:
            settings = json.load(f)
        if str(ctx.guild.id) not in settings:
            await ctx.send("This guild has not been set up.")
            return

        #get the guild id
        guild_id = ctx.guild.id

        #set the question time
        settings[str(guild_id)]['question_time'] = time

        #save the settings
        with open('./data/json/triviasettings.json', 'w') as f:
            json.dump(settings, f)

        await ctx.send("The question time has been set to " + str(time) + " seconds.")

    @triviaset.command(name="showanswer")
    async def triviaset_showanswer(self, ctx: commands.Context):
        #set the show answer for the current guild
        with open('./data/json/triviasettings.json') as f:
            settings = json.load(f)
        if str(ctx.guild.id) not in settings:
            await ctx.send("This guild has not been set up.")
            return

        #get the guild id
        guild_id = ctx.guild.id

        #set the show answer
        settings[str(guild_id)]['show_answer_after_question'] = not settings[str(guild_id)]['show_answer_after_question']

        #save the settings
        with open('./data/json/triviasettings.json', 'w') as f:
            json.dump(settings, f)

        await ctx.send("The show answer setting has been flipped.")

    @triviaset.command(name="showleaderboard")
    async def triviaset_showleaderboard(self, ctx: commands.Context):
        #set the show leaderboard for the current guild
        with open('./data/json/triviasettings.json') as f:
            settings = json.load(f)
        if str(ctx.guild.id) not in settings:
            await ctx.send("This guild has not been set up.")
            return

        #get the guild id
        guild_id = ctx.guild.id

        #set the show leaderboard
        settings[str(guild_id)]['show_leaderboard'] = not settings[str(guild_id)]['show_leaderboard']

        #save the settings
        with open('./data/json/triviasettings.json', 'w') as f:
            json.dump(settings, f)

        await ctx.send("The show leaderboard setting has been flipped.")

    @triviaset.command(name="pointminimum")
    async def triviaset_pointminimum(self, ctx: commands.Context, minimum: int):
        #set the point minimum for the current guild
        with open('./data/json/triviasettings.json') as f:
            settings = json.load(f)
        if str(ctx.guild.id) not in settings:
            await ctx.send("This guild has not been set up.")
            return

        #get the guild id
        guild_id = ctx.guild.id

        #set the point minimum
        settings[str(guild_id)]['point_minimum'] = minimum

        #save the settings
        with open('./data/json/triviasettings.json', 'w') as f:
            json.dump(settings, f)

        await ctx.send("The point minimum has been set to " + str(minimum))

    @triviaset.command(name="pointmaximum")
    async def triviaset_pointmaximum(self, ctx: commands.Context, maximum: int):
        #set the point maximum for the current guild
        with open('./data/json/triviasettings.json') as f:
            settings = json.load(f)
        if str(ctx.guild.id) not in settings:
            await ctx.send("This guild has not been set up.")
            return

        #get the guild id
        guild_id = ctx.guild.id

        #set the point maximum
        settings[str(guild_id)]['point_maximum'] = maximum

        #save the settings
        with open('./data/json/triviasettings.json', 'w') as f:
            json.dump(settings, f)

        await ctx.send("The point maximum has been set to " + str(maximum))

    @triviaset.group(name="custom")
    async def triviaset_custom(self, ctx: commands.Context):
        pass

    @triviaset_custom.command(name="list")
    async def triviaset_custom_list(self, ctx: commands.Context):
        #check if the current guild has been set up
        with open('./data/json/triviasettings.json') as f:
            settings = json.load(f)
        if str(ctx.guild.id) not in settings:
            await ctx.send("This guild has not been set up.")
            return

        #check if there is a folder for custom questions for this guild in the data/files/trivia folder
        if not os.path.exists('./data/files/trivia/' + str(ctx.guild.id)):
            await ctx.send("There are no custom questions for this guild.")
            return

        #get the custom questions for this guild
        custom_trivias = []
        for file in os.listdir('./data/files/trivia/' + str(ctx.guild.id)):
            if file.endswith('.csv'):
                custom_trivias.append(file)

        #send the custom questions
        await ctx.send("Custom questions for this guild:")
        for custom_trivia in custom_trivias:
            await ctx.send(custom_trivia)

        
    @triviaset_custom.command(name="upload", aliases=['add'])
    async def triviaset_custom_upload(self, ctx: commands.Context):
        #put the attachment in files/trivia/guild_id
        if len(ctx.message.attachments) == 0:
            await ctx.send("You must attach a file to this command.")
            return

        #get the attachment
        attachment = ctx.message.attachments[0]

        #check if the attachment is a text file
        if not attachment.filename.endswith('.csv'):
            await ctx.send("The file must be a csv (.csv) file.")
            return

        #get the guild id
        guild_id = ctx.guild.id

        #check if there is a folder for custom questions for this guild in the data/files/trivia folder
        if not os.path.exists('./data/files/trivia/' + str(guild_id)):
            os.mkdir('./data/files/trivia/' + str(guild_id))

        #get the file name
        file_name = attachment.filename

        #check if the file already exists
        if os.path.exists('./data/files/trivia/' + str(guild_id) + '/' + file_name):
            await ctx.send("The file already exists.")
            return

        #download the file
        await attachment.save('./data/files/trivia/' + str(guild_id) + '/' + file_name)

        await ctx.send("The file has been uploaded.")

    @triviaset_custom.command(name="delete", aliases=['remove'])
    async def triviaset_custom_delete(self, ctx: commands.Context, file_name: str):
        #check if the current guild has been set up
        with open('./data/json/triviasettings.json') as f:
            settings = json.load(f)
        if str(ctx.guild.id) not in settings:
            await ctx.send("This guild has not been set up.")
            return

        #check if there is a folder for custom questions for this guild in the data/files/trivia folder
        if not os.path.exists('./data/files/trivia/' + str(ctx.guild.id)):
            await ctx.send("There are no custom questions for this guild.")
            return

        #check if the file exists
        if not os.path.exists('./data/files/trivia/' + str(ctx.guild.id) + '/' + file_name + '.csv'):
            await ctx.send("The quiz does not exist.")
            return

        #delete the file
        os.remove('./data/files/trivia/' + str(ctx.guild.id) + '/' + file_name + '.csv')

        await ctx.send("The quiz has been deleted.")

    @triviaset_custom.command(name="clear", aliases=['deleteall', 'removeall'])
    async def triviaset_custom_clear(self, ctx: commands.Context):
        #check if the current guild has been set up
        with open('./data/json/triviasettings.json') as f:
            settings = json.load(f)
        if str(ctx.guild.id) not in settings:
            await ctx.send("This guild has not been set up.")
            return

        #check if there is a folder for custom questions for this guild in the data/files/trivia folder
        if not os.path.exists('./data/files/trivia/' + str(ctx.guild.id)):
            await ctx.send("There are no custom questions for this guild.")
            return

        #delete all files in the folder
        for file in os.listdir('./data/files/trivia/' + str(ctx.guild.id)):
            os.remove('./data/files/trivia/' + str(ctx.guild.id) + '/' + file)

        await ctx.send("All custom questions have been deleted.")

    @triviaset_custom.command(name="rename", aliases=['edit'])
    async def triviaset_custom_rename(self, ctx: commands.Context, file_name: str, new_file_name: str):
        #check if the current guild has been set up
        with open('./data/json/triviasettings.json') as f:
            settings = json.load(f)
        if str(ctx.guild.id) not in settings:
            await ctx.send("This guild has not been set up.")
            return

        #check if there is a folder for custom questions for this guild in the data/files/trivia folder
        if not os.path.exists('./data/files/trivia/' + str(ctx.guild.id)):
            await ctx.send("There are no custom questions for this guild.")
            return

        #check if the file exists
        if not os.path.exists('./data/files/trivia/' + str(ctx.guild.id) + '/' + file_name + '.csv'):
            await ctx.send("The quiz does not exist.")
            return

        #rename the file
        os.rename('./data/files/trivia/' + str(ctx.guild.id) + '/' + file_name + '.csv', './data/files/trivia/' + str(ctx.guild.id) + '/' + new_file_name + '.csv')

        await ctx.send("The quiz has been renamed.")

    @triviaset_custom.command(name="default", aliases=['defaultquiz'])
    async def triviaset_custom_default(self, ctx: commands.Context):
        #check if the current guild has been set up
        with open('./data/json/triviasettings.json') as f:
            settings = json.load(f)
        if str(ctx.guild.id) not in settings:
            await ctx.send("This guild has not been set up.")
            return

        #open default folder
        default = []
        for file in os.listdir('./data/files/trivia/default'):
            if file.endswith('.csv'):
                default.append(file)

        #send the custom questions
        await ctx.send("Default categories:")
        #join default with commas and remove the .csv extension
        await ctx.send(', '.join(default).replace('.csv', ''))

    @commands.command()
    async def emojitest(self, ctx):

        msg = await ctx.send("banana")
        await msg.add_reaction("<:1y_:927696490082762803>")
        await msg.add_reaction("<:2y_:927696490393128970>")
        await msg.add_reaction("<:3y_:927696490481217576>")
        await msg.add_reaction("<:4y_:927696490216972339>")


    @commands.has_permissions(manage_messages=True)
    @commands.command(name="trivia", aliases=['triv'])
    async def trivia(self, ctx: commands.Context, qNum: int, *, triviafile = None):
        #check if the current guild has been set up
        with open('./data/json/triviasettings.json') as f:
            settings = json.load(f)
        if str(ctx.guild.id) not in settings:
            await ctx.send("This guild has not been set up.")
            return

        #get the guild id
        guild_id = ctx.guild.id

        #open the trivia file
        with open('./data/files/trivia/' + str(guild_id) + '/' + triviafile + '.csv') as f:
            reader = csv.reader(f)
            questions = list(reader)
        #create a dictionary of random questions and answers size qNum questions from the csv
        random_questions = {}
        for i in range(0, qNum):
            random_questions[i] = questions[random.randint(0, len(questions)-1)]

        print(random_questions)



        scores = []
        scoreidlist = []

        embed = discord.Embed(title="Trivia", description="", color=0x8A00FF)
        embed.add_field(name="Game starting in:", value ="3 seconds!", inline=False)
        intromsg = await ctx.send(embed=embed)

        await asyncio.sleep(3)

        #get a guild object
        emojiguild = self.bot.get_guild(819286168729288716)

        await intromsg.delete()

        msg = None
        for i in random_questions:
            if msg is not None:
                await msg.delete()

            #store correct answer text
            correct_answer = random_questions[i][2]
            #store all answer choices
            answer_choices = random_questions[i][3:]
            #remove empty strings from the answer choices
            answer_choices = [x for x in answer_choices if x != '']

            print(answer_choices)
            #find the index of the correct answer
            correct_answer = answer_choices.index(correct_answer)+1


            #show the question for question_time seconds via embed
            embed = discord.Embed(title=random_questions[i][1], description="", color=0x8A00FF)
            embed.add_field(name="Answer choices will be revealed in:", value =str(settings[str(guild_id)]['question_time']) + " seconds!", inline=False)
            msg = await ctx.send(embed=embed)

            await asyncio.sleep(settings[str(guild_id)]['question_time'])

                
            #edit the embed
            embed = discord.Embed(title=random_questions[i][1], description="", color=0x8A00FF)

            #for each answer choice, add a field to the embed and start each field with a number corresponding to the answer choice
            for j in range(0, len(answer_choices)):
                embed.add_field(name=str(j+1) + ":", value =answer_choices[j], inline=False)

            emojis = ["<:1y_:927696490082762803>", "<:2y_:927696490393128970>", "<:3y_:927696490481217576>", "<:4y_:927696490216972339>", "<:5y_:927696490216964137>"]

            #if the length of answer choices is 1, only put one reaction
            if len(answer_choices) == 1:
                await msg.add_reaction(emojis[0])
            elif len(answer_choices) == 2:
                await msg.add_reaction(emojis[0])
                await msg.add_reaction(emojis[1])
            elif len(answer_choices) == 3:
                await msg.add_reaction(emojis[0])
                await msg.add_reaction(emojis[1])
                await msg.add_reaction(emojis[2])
            elif len(answer_choices) == 4:
                await msg.add_reaction(emojis[0])
                await msg.add_reaction(emojis[1])
                await msg.add_reaction(emojis[2])
                await msg.add_reaction(emojis[3])
            else:
                await msg.add_reaction(emojis[0])
                await msg.add_reaction(emojis[1])
                await msg.add_reaction(emojis[2])
                await msg.add_reaction(emojis[3])
                await msg.add_reaction(emojis[4])


            await msg.edit(embed=embed)

            #store reaction and userid in a stack
            queue = []
            while True:
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=settings[str(guild_id)]['answer_time'])
                    #translate emojis to 1 2 3 4 5
                    if str(reaction) == emojis[0]:
                        emoji = 1
                    elif str(reaction) == emojis[1]:
                        emoji = 2
                    elif str(reaction) == emojis[2]:
                        emoji = 3
                    elif str(reaction) == emojis[3]:
                        emoji = 4
                    elif str(reaction) == emojis[4]:
                        emoji = 5
                    queue.append((emoji, user.id))    
                    print("reaction recieved from " + str(user.id))       
                except asyncio.TimeoutError:
                    break

            # for every element in the queue, pull them out in reverse order and put them into a new queue, removing duplicates
            print("queue: " + str(queue))
            cleanqueue = []
            idlist = []

            for k in range(len(queue)):
                print("idlist: " + str(idlist))
                print("k: " + str(k))
                if queue[k][1] not in idlist:
                    cleanqueue.append(queue[k])
                    idlist.append(queue[k][1])
                    print("added " + str(queue[k][1]) + " to cleanqueue")


            print("correct answer index: " + str(correct_answer))

            print("cleanqueue: " + str(cleanqueue))

        
            for l in range(len(cleanqueue)):
                move = 0
                print("cleanqueue: " + str(cleanqueue))
                if cleanqueue[l][0] == correct_answer:
                    #score is max points divided by location in the queue
                    score = settings[str(guild_id)]['point_maximum'] / (l+1)        
                    move = 1            
                else:
                    score = -200
                    move = -1
                if cleanqueue[l][1] not in scoreidlist:
                    scores.append((cleanqueue[l][1], score, move))
                    scoreidlist.append(cleanqueue[l][1])
                else:
                    for i in range(len(scores)):
                        #search for a tuple with the user's id in the scores list and add the score to it
                        if scores[i][0] == cleanqueue[l][1]:
                            scores[i] = (scores[i][0], scores[i][1] + score, move)

            print("scores: " + str(scores))

            #sort the scores list by score
            scores.sort(key=lambda tup: tup[1], reverse=True)

            #send a leaderboard embed with the scores sorted by score
            embed = discord.Embed(title="Leaderboard", description="", color=0x00ff00)
            for m in range(len(scores)):

                if scores[m][2] == 1:
                    emojilb = get(emojiguild.emojis, name="Above")
                elif scores[m][2] == -1:
                    emojilb = get(emojiguild.emojis, name="Down")
                embed.add_field(name=str(m+1) + ":", value=self.bot.get_user(scores[m][0]).name + ": " + str(scores[m][1]) + " " + f"{emojilb}", inline=False)
            await msg.edit(embed=embed)

            #remove all reactions
            await msg.clear_reactions()

            await asyncio.sleep(5)



def setup(bot):
    bot.add_cog(Trivia(bot))