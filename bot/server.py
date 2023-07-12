"""Creating a server class with custom functions"""
import os
from dotenv import load_dotenv
class Server:
    """server class that is used during main.py"""
    def __init__(self):
        """creates the roles as variables from the .env file and 
        also finds the id of the roles through the .env file """
        load_dotenv()
        VERIFIED_ROLE = os.getenv('DISCORD_VERIFIED_ROLE')
        ALUMNI_ROLE = os.getenv('DISCORD_ALUMNI_ROLE')
        GRADUATE_ROLE = os.getenv('DISCORD_GRADUATE_ROLE')
        UNDERGRADUATE_ROLE = os.getenv('DISCORD_UNDERGRADUATE_ROLE')
        FACULTY_ROLE = os.getenv('DISCORD_FACULTY_ROLE')
        GUILD = os.getenv('DISCORD_GUILD')
        self.server = None
        self.verified_role_id: int = int(VERIFIED_ROLE)
        self.undergraduate_role_id = int(UNDERGRADUATE_ROLE)
        self.graduate_role_id = int(GRADUATE_ROLE)
        self.alumni_role_id = int(ALUMNI_ROLE)
        self.faculty_role_id = int(FACULTY_ROLE)
        self.guild_id: int = int(GUILD)
    def get_member(self, ctx):
        """returns server id"""
        return self.server.get_member(ctx.user.id)
    def get_roles(self, affiliation):
        """sets the roles as verified and set affiliation"""
        print(affiliation)
        affiliation_role_id = 0
        if affiliation == "undergraduate":
            affiliation_role_id = self.undergraduate_role_id
        elif affiliation == "graduate":
            affiliation_role_id = self.graduate_role_id
        elif affiliation == "alumni":
            affiliation_role_id = self.alumni_role_id
        elif affiliation == "faculty":
            affiliation_role_id = self.faculty_role_id

        return [
            self.server.get_role(self.verified_role_id),
            self.server.get_role(affiliation_role_id)
        ]

    def get_guild(self) -> int:
        """returns server id"""
        return self.guild_id
