from __future__ import print_function

import os
import os.path

import discord
from discord.ext import commands
from dotenv import load_dotenv

import shortuuid

from sendCode import *
from db import *


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# client = discord.Client()

bot = commands.Bot(command_prefix='!', intents=discord.Intents(
    messages=True, guilds=True))


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.id == GUILD:
            break
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@bot.command(name="verify")
async def verify(ctx, *args):
    if(ctx.guild == None):
        if(len(args) < 2):
            await ctx.author.send("format: !verify <Your UCR email> <Your Full Name>🤔")
            return
        email = args[0]
        firstName = args[1]
        name = args[1]

        for i in range(2, len(args)):
            name += " "+args[i]
        if not "@ucr.edu" in email:
            await ctx.author.send("Please use your ucr email🥺")
            return

        discordID = str(ctx.message.author)

        try:
            user = getUser(email, name, str(ctx.message.author))
            if(user == None):
                try:
                    uuid = shortuuid.ShortUUID().random(length=8)
                    # print(uuid)
                    sendEmail(email, uuid)
                    createUser(email, name, discordID, uuid)
                    await ctx.author.send("Hi "+firstName+" your verification code is sent to your email at "+email + "\nPlease send me the verification code in this format: !code < Your Code >😇")
                except Exception as error:
                    print(error)
                    return
            else:
                if(user[3] == discordID):
                    if(user[4]):
                        await ctx.author.send("Hi "+firstName+" your discord is already verified!😝")
                    elif(user[1] != email):
                        updateEmail(user[3], email)
                        await ctx.author.send("Hi "+firstName+" your verification code is resent to your email at "+email+"🫡")
                    else:
                        sendEmail(email, user[2])
                        await ctx.author.send("Hi "+firstName+" your verification code is resent to your email at "+email+"🫡")
                elif(user[1] == email):
                    await ctx.author.send("Hi "+firstName+" your email "+email+" has already being connect to " + user[0] + " ("+user[3]+")😅")

        except Exception as error:
            print(error)
            return


@bot.command(name="code")
async def code(message, *args):
    if(len(args) < 1):
        return
    if(message.guild == None):
        try:
            user = getUser(email="", name="", discordID=str(message.author))
            if(user[4]):
                await message.author.send("You are already verified!!😊")
                return
        except Exception as error:
            print(error)
        if(verifyUser(str(message.author), str(args[0]))):
            await message.author.send("Successfully verified!!🥳")
        else:
            await message.author.send("Fail verification😭")


if __name__ == '__main__':
    bot.run(TOKEN)
