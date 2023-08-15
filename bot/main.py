import os
from dotenv import load_dotenv
from bot.firebase_db import Firestore
from bot.sendgrid_email import Sendgrid
from bot.server import Server
import discord
from discord.ext import commands
from discord import Client
from discord import Guild
from discord import Embed
from discord import Color
from discord import DMChannel

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot: Client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

FIRESTORE = Firestore()
SENDGRID = Sendgrid()
GUILD = Server()


@bot.event
async def on_ready():
    """
    Event triggered when the bot is ready.

    This function sets the server as the guild for later use.
    """
    for guild in bot.guilds:
        if guild.id == GUILD.get_guild():
            GUILD.server: Guild = guild
    try:
        await bot.tree.sync()
    except ConnectionError as e:
        print(e)


@bot.event
async def on_member_join(member):
    """
    Event triggered when a member joins the server.

    This function sends a welcome message to the new member with instructions for verification.
    """
    if member.guild == GUILD.server:
        embed: Embed = Embed(
            title="Welcome to ACM!",
            description="To gain access to the full server, please run the following slash commands.",
            color=Color.blue()  # Set the color of the embed (optional)
        )

        # Add fields to the embed
        embed.add_field(name="/verify",
                        value="You will receive an 8-digit code in your email",
                        inline=False)
        embed.add_field(
            name="/code",
            value="Please enter that code in this command for verification",
            inline=True)

        await member.send(embed=embed)


@bot.event
async def on_message(message):
    """
    Event triggered when a message is sent.

    This function runs when a user sends a message without using slash commands.
    """
    if isinstance(message.channel, DMChannel) and message.author != bot.user:
        if "verify" in message.content.lower() or "code" in message.content.lower():
            await message.channel.send(
                "Please use the slash commands. The format is \"/\" followed by the command of your choice.")


def main():
    """
    Main function to run the bot with the .env token.
    """
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
