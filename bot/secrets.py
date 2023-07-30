import os
import re
import shortuuid
from dotenv import load_dotenv
from bot.firebase_db import Firestore
from bot.sendgrid_email import Sendgrid
from bot.server import Server
import discord
from discord.ext import commands
from discord import Interaction, Message, Reaction, Member, Role, Guild, TextChannel, Client, utils


class Secrets:
       
    def __init__(self, bot: Client):
        load_dotenv()
        self.bot: Client = bot
        self.guild_id: int = int(os.getenv('DISCORD_PROJECT_GUILD'))
        self.bot_role_id: int = int(os.getenv('DISCORD_BOT_ROLE'))
        self.bitbybit_role_id: int = int(os.getenv('DISCORD_BITBYBIT_ROLE'))
        self.membership_role_id: int = int(os.getenv('DISCORD_MEMBERSHIP_PORTAL_ROLE'))
        self.rmate_role_id: int = int(os.getenv('DISCORD_RMATE_ROLE'))


    async def get_member(self, user_id):
        """returns a member from a specific guild"""
        guild = await self.bot.fetch_guild(self.guild_id)
        if guild:
            return await guild.fetch_member(user_id)
        else:
            return None


    def has_role(self, user, role_id):
        role = discord.utils.get(user.roles, id = role_id)
        return role is not None
    
    async def send_secrets(self, ctx, project):
        member_id = ctx.user.id  # Get the member's ID from the context
        member = await self.get_member(member_id)  # Get the member using their ID
        guild = self.bot.get_guild(self.guild_id)
        if guild is None:
            print(f"Could not find guild with id {self.guild_id}")
            return
        
        if member is None:
            print(f"Could not find member with id {ctx.user.id} in guild {self.guild_id}")
            return
        
        if self.has_role(member, self.bot_role_id) and project == "Discord Bot":
            with open('secrets/Discord Bot.env','rb') as fp:
                await ctx.response.send_message(file=discord.File(fp, filename=f"{project}.env"), ephemeral=True)
            return
        if self.has_role(member, self.bitbybit_role_id) and project == "bitByBIT":
            with open('secrets/bitByBIT.env','rb') as fp:
                await ctx.response.send_message(file=discord.File(fp, filename=f"{project}.env"), ephemeral=True)
            return
        if self.has_role(member, self.rmate_role_id) and project == "R'Mate":
            with open("secrets/R'Mate.env",'rb') as fp:
                await ctx.response.send_message(file=discord.File(fp, filename=f"{project}.env"), ephemeral=True)
            return
        if self.has_role(member, self.membership_role_id) and project == "Membership Portal":
            with open('secrets/Membership Portal.env','rb') as fp:
                await ctx.response.send_message(file=discord.File(fp, filename=f"{project}.env"), ephemeral=True)
            return

        await ctx.response.send_message("Wrong role!", ephemeral=True)
        return