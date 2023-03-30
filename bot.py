import os
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

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

FIRESTORE = Firestore()
SENDGRID = Sendgrid()
GUILD = Guild()


@bot.event
async def on_ready():
    for guild in bot.guilds:
        GUILD.server = guild
    try:
        syced = await bot.tree.sync()
        print(len(syced))
    except Exception as e:
        print(e)


@bot.tree.command(name="verify")
@app_commands.describe(name="your full name", email="your UCR email")
async def verify(ctx: discord.Interaction, name: str, email: str):
    # TODO CLEANUP DATA FETCHING
    if not "@ucr.edu" in email:
        await ctx.response.send_message("Please use your ucr email 🥺",
                                        ephemeral=True)
        return

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
    code="The 16 charactor verification code send to your email")
# TODO HARDCODE THE CODE PART SINCE ANYTHING THEY SEND AFTER WE DONT CARE ABOUT
async def code(ctx: discord.interactions, code: str):
    try:
        if FIRESTORE.verifyUser(str(ctx.user), code):
            await ctx.response.send_message("Successfully verified 🥳!!",
                                            ephemeral=True)
            await giveRole(ctx)
    except Exception as error:
        await ctx.response.send_message("Failed verification 😭",
                                        ephemeral=True)


async def giveRole(ctx):
    member = GUILD.get_member(ctx)
    role = GUILD.get_role()
    await member.add_roles(role)
#wow

if __name__ == '__main__':
    bot.run(TOKEN)
