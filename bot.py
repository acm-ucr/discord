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

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

FIRESTORE = Firestore()
SENDGRID = Sendgrid()
GUILD = Guild()


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.id == GUILD.get_guild():
            GUILD.server = guild
    try:
        await bot.tree.sync()
    except Exception as e:
        print(e)


@bot.tree.command(name="verify")
@app_commands.describe(name="Full Name", email="UCR Email")
@app_commands.choices(affiliation=[
    app_commands.Choice(name="Undergraduate", value="undergraduate"),
    app_commands.Choice(name="Graduate", value="graduate"),
    app_commands.Choice(name="Alumni", value="alumni"),
    app_commands.Choice(name="Faculty", value="faculty"),
])
async def verify(
    ctx: discord.Interaction,
    name: str,
    email: str,
    affiliation: app_commands.Choice[str],
) -> None:
    name = name.strip()
    if not re.search("[a-zA-Z]\s[a-zA-Z]", name):
        await ctx.response.send_message(
            "Please provide a first and last name 🥺", ephemeral=True)
        return

    email = email.strip().lower()
    if not re.search("[a-z]{3,5}\d{3}@ucr.edu", email):
        await ctx.response.send_message("Please use your UCR email 🥺",
                                        ephemeral=True)
        return

    discord = str(ctx.user)

    user_id, user_data = FIRESTORE.getUser(discord, email)

    if user_id == "Too Many or Not Enough Documents Fetched":
        await ctx.response.send_message(
            f"There is an error with the number of accounts associated with this Discord or Email. Please contact an ACM officer for further assistance",
            ephemeral=True)

    elif user_data == {}:
        uuid = shortuuid.ShortUUID().random(length=8)
        SENDGRID.sendEmail(email, name, discord, uuid)
        FIRESTORE.createUser(email, name, discord, uuid, affiliation.value)

        await ctx.response.send_message(
            f"Hi **{name}** your verification code is sent to your email at **{email}** \nPlease send the verification code in this format: `/code <8 Character Code> 😇`",
            ephemeral=True)

    else:
        await ctx.response.send_message(
            f"Hi **{name}**, this email has already been sent a verification email at {email}. Please check your email for a verification code! If you require assistance please contact an ACM officer!",
            ephemeral=True)


@bot.tree.command(name="code")
@app_commands.describe(code="8 Character Code Sent Via Email")
async def code(ctx: discord.Interaction, code: str) -> None:
    if not re.search("\w{8}", code):
        await ctx.response.send_message(
            "The provided code is not 8 characters long 😭!", ephemeral=True)
        return
    try:
        verified, result = FIRESTORE.verifyUser(str(ctx.user), code)
        if result.get("error",
                      "") == "Too Many or Not Enough Documents Fetched":
            await ctx.response.send_message(
                f"There is an error with the number of accounts associated with this Discord or Email. Please contact an ACM officer for further assistance",
                ephemeral=True)
            return
        if verified:
            member = GUILD.get_member(ctx)
            verified_role, affliation_role = GUILD.get_roles(
                result["affiliation"])
            await member.add_roles(verified_role, affliation_role)
            await ctx.response.send_message("Successfully verified 🥳!!",
                                            ephemeral=True)
        else:
            await ctx.response.send_message(
                "We were unable to verify your account 😭!", ephemeral=True)
    except Exception as error:
        await ctx.response.send_message("Failed verification 😭",
                                        ephemeral=True)
        print(error)


if __name__ == '__main__':
    bot.run(TOKEN)
