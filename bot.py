import os
import re
import discord
import shortuuid
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from firebase_db import Firestore
from sendgrid_email import Sendgrid
from guild import Guild

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(intents=discord.Intents.all())

FIRESTORE = Firestore()
SENDGRID = Sendgrid()
GUILD = Guild()


@bot.event
async def on_ready():
    for guild in bot.guilds:
        GUILD.server = guild
    try:
        await bot.tree.sync()
    except Exception as e:
        print(e)


@bot.tree.command(name="verify")
@app_commands.describe(name="Full Name", email="UCR Email")
async def verify(ctx: discord.Interaction, name: str, email: str) -> None:

    name = name.strip()
    if not re.search("[a-zA-Z]\s[a-zA-Z]", name):
        await ctx.response.send_message("Please provide a first and last name 🥺",
                                         ephemeral=True)

    email = email.strip().lower()
    if not re.search("[a-z]{3,5}\d{3}@ucr.edu", email):
        await ctx.response.send_message("Please use your UCR email 🥺",
                                         ephemeral=True)
    
    

    discord = str(ctx.user)

    __, user_data = FIRESTORE.getUser(discord)

    if user_data == {}:
        uuid = shortuuid.ShortUUID().random(length=16)
        SENDGRID.sendEmail(email, uuid)
        FIRESTORE.createUser(email, name, discord, uuid)

        await ctx.response.send_message(
            f"Hi **{name}** your verification code is sent to your email at **{email}** \nPlease send the verification code in this format: `!code <16 Character Code> 😇`",
            ephemeral=True)


@bot.tree.command(name="code")
@app_commands.describe(
    code="16 Character Code Sent Via Email")
async def code(ctx: discord.interactions, code: str):
    if not re.search("\w{16}", code):
        await ctx.response.send_message("The provided code is not 16 characters long 😭!",
                                            ephemeral=True)
        return
    try:
        if FIRESTORE.verifyUser(str(ctx.user), code):
            await ctx.response.send_message("Successfully verified 🥳!!",
                                            ephemeral=True)
            await giveRole(ctx)
        else:
            await ctx.response.send_message("We were unable to verify your account 😭!",
                                            ephemeral=True)
    except Exception as error:
        await ctx.response.send_message("Failed verification 😭",
                                        ephemeral=True)


async def giveRole(ctx):
    member = GUILD.get_member(ctx)
    role = GUILD.get_role()
    await member.add_roles(role)

if __name__ == '__main__':
    bot.run(TOKEN)
