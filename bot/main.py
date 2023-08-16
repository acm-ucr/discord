"""Discord Bot: Interacts with the Discord API to provide different functionalities"""

import os
from dotenv import load_dotenv
from bot.firebase_db import Firestore
from bot.sendgrid_email import Sendgrid
from bot.server import Server
from bot.welcome import Welcome
from bot.verification import Verification
from bot.secrets import Secrets
from discord.ext import commands
from discord import Intents, Client, app_commands, Interaction

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot: Client = commands.Bot(command_prefix="!", intents=Intents.all())

FIRESTORE = Firestore()
SENDGRID = Sendgrid()
GUILD = Server(bot)
WELCOME = Welcome()
VERIFICATION = Verification(bot)
SECRETS = Secrets(bot)


@bot.event
async def on_ready():
    """Event triggered when the bot is ready"""
    try:
        await bot.tree.sync()
    except ConnectionError as e:
        print(e)


@bot.event
async def on_member_join(member):
    """Runs when a new member joins the Discord"""
    await WELCOME.send_welcome_message(member)


@bot.tree.command(name="verify")
@app_commands.describe(name="Full Name", email="UCR Email")
@app_commands.choices(affiliation=[
    app_commands.Choice(name="Undergraduate", value="undergraduate"),
    app_commands.Choice(name="Graduate", value="graduate"),
    app_commands.Choice(name="Alumni", value="alumni"),
    app_commands.Choice(name="Faculty", value="faculty"),
])
async def verify(
    ctx: Interaction,
    name: str,
    email: str,
    affiliation: app_commands.Choice[str],
) -> None:
    """Initiate verification process"""
    await VERIFICATION.verify(ctx, name, email, affiliation)


@bot.tree.command(name="code")
@app_commands.describe(code="8 Character Code Sent Via Email")
async def code(ctx: Interaction, codestring: str) -> None:
    """Accept verification codes"""
    await VERIFICATION.code(ctx, codestring)


@bot.tree.command(name="secrets")
@app_commands.choices(projects=[
    app_commands.Choice(name="Discord Bot", value="Discord Bot"),
    app_commands.Choice(name="bitByBIT", value="bitByBIT"),
    app_commands.Choice(name="R'Mate", value="R'Mate"),
    app_commands.Choice(name="Membership Portal", value="Membership Portal"),
])
@commands.has_any_role("R'Mate", 'bitByBIT', 'Membership Portal',
                       'Discord Bot')
async def secrets(
    ctx: Interaction,
    project: app_commands.Choice[str],
) -> None:
    """Send environment secrets to members"""
    await SECRETS.get_secrets(ctx, project)


def main():
    """Run Bot"""
    bot.run(TOKEN)
