import os
from dotenv import load_dotenv
from discord import Guild

class Server:
    """Utility class for managing server-related information and operations."""

    def __init__(self):
        """Initialize server-related settings from environment variables."""
        load_dotenv()
        VERIFIED_ROLE = os.getenv('DISCORD_VERIFIED_ROLE')
        ALUMNI_ROLE = os.getenv('DISCORD_ALUMNI_ROLE')
        GRADUATE_ROLE = os.getenv('DISCORD_GRADUATE_ROLE')
        UNDERGRADUATE_ROLE = os.getenv('DISCORD_UNDERGRADUATE_ROLE')
        FACULTY_ROLE = os.getenv('DISCORD_FACULTY_ROLE')
        GUILD = os.getenv('DISCORD_GUILD')
        self.server: Guild = None
        self.verified_role_id: int = int(VERIFIED_ROLE)
        self.undergraduate_role_id: int = int(UNDERGRADUATE_ROLE)
        self.graduate_role_id: int = int(GRADUATE_ROLE)
        self.alumni_role_id: int = int(ALUMNI_ROLE)
        self.faculty_role_id: int = int(FACULTY_ROLE)
        self.guild_id: int = int(GUILD)

    def get_member(self, ctx):
        """Get a member from the server using the context.

        Args:
            ctx (Context): The context of the command.

        Returns:
            Member: The corresponding member in the server.
        """
        return self.server.get_member(ctx.user.id)

    def get_roles(self, affiliation):
        """Get a list of roles based on the user's affiliation.

        Args:
            affiliation (str): The affiliation of the user.

        Returns:
            list: A list of role objects.
        """
        print(affiliation)
        affiliation_role_id: int = 0
        if affiliation == "undergraduate":
            affiliation_role_id: int = self.undergraduate_role_id
        elif affiliation == "graduate":
            affiliation_role_id: int = self.graduate_role_id
        elif affiliation == "alumni":
            affiliation_role_id: int = self.alumni_role_id
        elif affiliation == "faculty":
            affiliation_role_id: int = self.faculty_role_id

        return [
            self.server.get_role(self.verified_role_id),
            self.server.get_role(affiliation_role_id)
        ]

    def get_guild(self) -> int:
        """Get the ID of the Discord server (guild).

        Returns:
            int: The ID of the Discord server (guild).
        """
        return self.guild_id
