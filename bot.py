import os
import discord
import shortuuid
from discord.ext import commands
from dotenv import load_dotenv
from firebase_db import Firestore
from sendgrid_email import Sendgrid
from guild import Guild

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!',
                   intents=discord.Intents(messages=True,
                                           guilds=True,
                                           members=True))

FIRESTORE = Firestore()
SENDGRID = Sendgrid()
GUILD = Guild(bot = bot)

@bot.event
async def on_ready():
    print(bot.guilds, type(bot.guilds))
    for guild in bot.guilds:
        GUILD.server = guild


@bot.command(name="verify")
async def verify(ctx, *args):
    # TODO CLEANUP DATA FETCHING
    if (ctx.guild == None):
        if (len(args) < 2):
            await ctx.author.send(
                "Please use the following format: `!verify <Your UCR email> <Your Full Name>` 🤔"
            )
            return
        email = args[0]
        name = args[1]

        for i in range(2, len(args)):
            name += " " + args[i]
        if not "@ucr.edu" in email:
            await ctx.author.send("Please use your ucr email 🥺")
            return

        discord = str(ctx.message.author)

        __, user_data = FIRESTORE.getUser(discord)

        if user_data == {}:
            uuid = shortuuid.ShortUUID().random(length=16)
            SENDGRID.sendEmail(email, uuid)
            FIRESTORE.createUser(email, name, discord, uuid)

            await ctx.author.send(
                f"Hi **{name}** your verification code is sent to your email at **{email}** \nPlease send the verification code in this format: `!code <16 Character Code> 😇`"
            )


@bot.command(name="code")
# TODO HARDCODE THE CODE PART SINCE ANYTHING THEY SEND AFTER WE DONT CARE ABOUT
async def code(ctx, *args):
    if (ctx.guild == None and len(args) >= 1):
        try:
            if FIRESTORE.verifyUser(str(ctx.author), args[0]):
                await ctx.author.send("Successfully verified 🥳!!")
                await giveRole(ctx)
        except Exception as error:
            print("LINE 64", error)
            await ctx.author.send("Failed verification 😭")


async def giveRole(ctx):
    member = GUILD.get_member(ctx)
    role = GUILD.get_role()
    await member.add_roles(role)


if __name__ == '__main__':
    bot.run(TOKEN)
