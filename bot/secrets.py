from discord.ext import commands
from discord import app_commands
from discord import Guild
from discord import Member
from discord import Role
from discord import Interaction

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
    ctx: Interaction,
    project: app_commands.Choice[str],
) -> None:
    """Display secrets based on user's roles and selected project.

    Args:
        ctx (Interaction): The context of the interaction.
        project (app_commands.Choice[str]): The selected project.

    Returns:
        None
    """
    user_guilds: list[Guild] = ctx.user.mutual_guilds
    for guild in user_guilds:
        if guild.id == 984881520697278514:
            user: Member  = guild.get_member(ctx.user.id)
            user_roles: list[Role] = user.roles
    for role in user_roles:
        if (role.name == project.value) and (role.name == "Discord Bot"):
            await ctx.response.send_message("DISCORD BOT FAKE SECRET",
                                            ephemeral=True)
            return
        if ((role.name == project.value) and (role.name == "bitByBIT")):
            await ctx.response.send_message("bitByBIT FAKE SECRET",
                                            ephemeral=True)
            return
        if ((role.name == project.value) and (role.name == "R'Mate")):
            await ctx.response.send_message("R'Mate FAKE SECRET",
                                            ephemeral=True)
            return
        if ((role.name == project.value)
                and (role.name == "Membership Portal")):
            await ctx.response.send_message("Membership Portal FAKE SECRET",
                                            ephemeral=True)
            return
        await ctx.response.send_message("Wrong role!", ephemeral=True)
    return
