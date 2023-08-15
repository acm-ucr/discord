import re
import shortuuid
import discord
from discord import app_commands
from discord import Member
from discord import Role
from discord import Interaction
from discord import DMChannel

async def isDM(ctx):
    """Check if the command is being used in a DM channel.

    Args:
        ctx (Interaction): The context of the interaction.

    Returns:
        bool: True if the command is used in a DM, False otherwise.
    """
    if not isinstance(ctx.channel, DMChannel):
        await ctx.response.send_message("DM me this command to use it.",
                                        ephemeral=True)
        return False
    return True

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
    """Verify a user's identity and affiliation.

    Args:
        ctx (Interaction): The context of the interaction.
        name (str): Full name of the user.
        email (str): UCR email of the user.
        affiliation (app_commands.Choice[str]): Affiliation of the user.

    Returns:
        None
    """
    name: str = name.strip()
    if not re.search(r"[a-zA-Z]r\s[a-zA-Z]", name):
        await ctx.response.send_message(
            "Please provide a first and last name 🥺", ephemeral=True)
        return

    email: str = email.strip().lower()
    if not re.search(r"[a-z]{3,5}\d{3,4}@ucr.edu", email):
        await ctx.response.send_message("Please use your UCR email 🥺",
                                        ephemeral=True)
        return

    discorduser: str = str(ctx.user)

    user_arr: list = FIRESTORE.getUser(discorduser, email)

    user_id: str = user_arr[0]
    user_data: dict = user_arr[1]

    if user_id == "Too Many or Not Enough Documents Fetched":
        await ctx.response.send_message(
            "There is an error with the number of accounts associated with this Discord or Email."
            " Please contact an ACM officer for further assistance",
            ephemeral=True)

    elif user_data == {}:
        uuid: str = shortuuid.ShortUUID().random(length=8)
        SENDGRID.sendEmail(email, name, discord, uuid)
        FIRESTORE.createUser(email, name, discord, uuid, affiliation.value)

        await ctx.response.send_message(
            f"Hi **{name}** your verification code is sent to your email at **{email}** \nPlease"
            " send the verification code in this format: `/code <8 Character Code> 😇`",
            ephemeral=True)

    else:
        await ctx.response.send_message(
            f"Hi **{name}**, this email has already been sent a verification email at {email}."
            " Please check your email for a verification code! "
            "If you require assistance please contact"
            " an ACM officer!",
            ephemeral=True)


@bot.tree.command(name="code")
@app_commands.describe(code="8 Character Code Sent Via Email")
async def code(ctx: Interaction, codestring: str) -> None:
    """Verify a user based on the verification code.

    Args:
        ctx (Interaction): The context of the interaction.
        codestring (str): The verification code.

    Returns:
        None
    """
    if not await isDM(ctx):
        return
    if not re.search(r"\w{8}", codestring):
        await ctx.response.send_message(
            "The provided code is not 8 characters long 😭!", ephemeral=True)
        return
    try:
        verify_arr: list = FIRESTORE.verifyUser(str(ctx.user), code)
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
            member: Member = GUILD.get_member(ctx)
            role_arr: list = GUILD.get_roles(
                result["affiliation"])
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
