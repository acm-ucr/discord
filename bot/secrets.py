from discord.ext import commands
from discord import Interaction, Role, Guild, Member, app_commands
from dotenv import load_dotenv

class Secrets:
    def __init__(self, bot):
        load_dotenv()
        ACM_SOFTWARE_DEVELOPMENT_ID = os.getenv('DISCORD_ACM_SOFTWARE_DEVELOPMENT_ID')
        self.guild_id: int = int(ACM_SOFTWARE_DEVELOPMENT_ID)
        self.guild = bot.get_guild(self.guild_id)

    async def get_secrets(
        self,
        ctx: Interaction,
        project: app_commands.Choice[str],
    ) -> None:
        """Display secrets based on user's roles and selected project"""
        user_guilds: list[Guild] = ctx.user.mutual_guilds
        user: Member  = self.guild.get_member(ctx.user.id)
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
