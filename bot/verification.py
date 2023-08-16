"""Class to handle verification process"""

import re
from shortuuid import ShortUUID
from discord import DMChannel, Interaction, Role, Member, app_commands
from bot.firebase_db import Firestore
from bot.sendgrid_email import Sendgrid
from bot.server import Server


class Verification:
    """Class to handle verification process"""

    def __init__(self, bot):
        self.FIRESTORE = Firestore()
        self.SENDGRID = Sendgrid()
        self.GUILD = Server(bot)

    async def isDM(self, ctx) -> bool:
        """Check if the command is being used in a DM channel"""
        if not isinstance(ctx.channel, DMChannel):
            await ctx.response.send_message("DM me this command to use it.",
                                            ephemeral=True)
            return False
        return True

    async def verify(
        self,
        ctx: Interaction,
        name: str,
        email: str,
        affiliation: app_commands.Choice[str],
    ) -> None:
        """Verify a user's identity and affiliation"""
        name: str = name.strip()
        if not re.search(r"[a-zA-Z]\s[a-zA-Z]", name):
            await ctx.response.send_message(
                "Please provide a first and last name 😁", ephemeral=True)
            return

        email: str = email.strip().lower()
        if not re.search(r"[a-z]{3,5}\d{3,4}@ucr.edu", email):
            await ctx.response.send_message("Please use your UCR email 😁",
                                            ephemeral=True)
            return

        discord: str = str(ctx.user)
        user_arr: list = self.FIRESTORE.getUser(discord, email)
        user_id: str = user_arr[0]
        user_data: dict = user_arr[1]

        if user_id == "Too Many or Not Enough Documents Fetched":
            await ctx.response.send_message(
                "There is an error with the number of accounts associated with this Discord"
                "or Email. Please contact an ACM officer for further assistance",
                ephemeral=True)

        elif user_data == {}:
            uuid: str = ShortUUID().random(length=8)
            self.SENDGRID.sendEmail(email, name, discord, uuid)
            self.FIRESTORE.createUser(email, name, discord, uuid,
                                      affiliation.value)

            await ctx.response.send_message(
                f"Hi **{name}** your verification code is sent to your email at **{email}** "
                "\nPlease send the verification code in this format: `/code <8 Character Code> 😇`",
                ephemeral=True)

        else:
            await ctx.response.send_message(
                f"Hi **{name}**, this email has already been sent a verification email at {email}."
                " Please check your email for a verification code! "
                "If you require assistance please contact"
                " an ACM officer!",
                ephemeral=True)

    async def code(self, ctx: Interaction, code: str) -> None:
        """Verify a user based on the verification code"""
        if not await self.isDM(ctx):
            return
        if not re.search(r"\w{8}", code):
            await ctx.response.send_message(
                "The provided code is not 8 characters long 😭!",
                ephemeral=True)
            return
        try:
            verify_arr: list = self.FIRESTORE.verifyUser(str(ctx.user), code)
            verified: bool = verify_arr[0]
            result: dict = verify_arr[1]
            if result.get("error",
                          "") == "Too Many or Not Enough Documents Fetched":
                await ctx.response.send_message(
                    "There is an error with the number of accounts associated"
                    " with this Discord or Email."
                    " Please contact an ACM officer for further assistance",
                    ephemeral=True)
                return
            if verified:
                member: Member = self.GUILD.get_member(ctx)
                role_arr: list = self.GUILD.get_roles(result["affiliation"])
                verified_role: Role = role_arr[0]
                affliation_role: Role = role_arr[1]
                await member.add_roles(verified_role, affliation_role)
                await ctx.response.send_message("Successfully verified 🥳!!",
                                                ephemeral=True)
            else:
                await ctx.response.send_message(
                    "We were unable to verify your account 😭!", ephemeral=True)
        except ConnectionError as error:
            await ctx.response.send_message("Failed verification 😭",
                                            ephemeral=True)
            print(error)
