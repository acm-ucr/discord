import os
import re
import discord
import shortuuid
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from bot.firebase_db import Firestore
from bot.sendgrid_email import Sendgrid
from bot.server import Server

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

FIRESTORE = Firestore()
SENDGRID = Sendgrid()
GUILD = Server()


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.id == GUILD.get_guild():
            GUILD.server = guild
    try:
        await bot.tree.sync()
    except Exception as e:
        print(e)


@bot.command()
@commands.has_any_role('Discord Bot')
async def discordbotsecrets(ctx):
    user = ctx.author
    await user.send("Discord Bot fakesecret")
    return


@bot.command()
@commands.has_any_role('Membership Portal')
async def membershipportalsecrets(ctx):
    user = ctx.author
    await user.send("Membership fakesecret")
    return


@bot.command()
@commands.has_any_role("R'Mate")
async def rmatesecrets(ctx):
    user = ctx.author
    await user.send("R'Mate fakesecret")
    return


@bot.command()
@commands.has_any_role('bitByBIT')
async def bitbybitsecrets(ctx):
    user = ctx.author
    await user.send("bitByBIT fakesecret")
    return


@bot.command()
@commands.has_any_role("R'Mate", 'bitByBIT', 'Membership Portal',
                       'Discord Bot')
async def secret(ctx):
    user = ctx.author
    user_roles = user.roles
    for role in user_roles:
        if role.name == "R'Mate":
            await user.send("rmate fakesecret")
            return
        elif role.name == "Membership Portal":
            await user.send("mem fakesecret")
            return
        elif role.name == "bitByBIT":
            await user.send("bit fakesecret")
            return
        elif role.name == "Discord Bot":
            await user.send("discordbot fakesecret")
            return
    await user.send("didn't pass")


@bot.tree.command(name="secrets")
@app_commands.choices(project=[
    app_commands.Choice(name="Discord Bot", value="Discord Bot"),
    app_commands.Choice(name="bitByBIT", value="bitByBIT"),
    app_commands.Choice(name="R'Mate", value="R'Mate"),
    app_commands.Choice(name="Membership Portal", value="Membership Portal"),
])
@commands.has_any_role("R'Mate", 'bitByBIT', 'Membership Portal',
                       'Discord Bot')
async def secrets(
    ctx: discord.Interaction,
    project: app_commands.Choice[str],
) -> None:
    user_guilds = ctx.user.mutual_guilds
    for guild in user_guilds:
        if (guild.id == 984881520697278514):
            user = guild.get_member(ctx.user.id)
            user_roles = user.roles
    for role in user_roles:
        if ((role.name == project.value) and (role.name == "Discord Bot")):
            await ctx.response.send_message("DISCORD BOT FAKE SECRET",
                                            ephemeral=True)
            return
        elif ((role.name == project.value) and (role.name == "bitByBIT")):
            await ctx.response.send_message("bitByBIT FAKE SECRET",
                                            ephemeral=True)
            return
        elif ((role.name == project.value) and (role.name == "R'Mate")):
            await ctx.response.send_message("R'Mate FAKE SECRET",
                                            ephemeral=True)
            return
        elif ((role.name == project.value)
              and (role.name == "Membership Portal")):
            await ctx.response.send_message("Membership Portal FAKE SECRET",
                                            ephemeral=True)
            return
        else:
            await ctx.response.send_message("Wrong role!", ephemeral=True)
    return


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
    if not re.search("[a-z]{3,5}\d{3,4}@ucr.edu", email):
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


def main():
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
