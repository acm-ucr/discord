import os
from dotenv import load_dotenv



class Guild:

    def __init__(self, bot):
        load_dotenv()
        ROLE = os.getenv('DISCORD_ROLE')
        GUILD = os.getenv('DISCORD_GUILD')

        self.server = None
        self.role_id = ROLE
        self.guild_id = GUILD
    
    def get_member(self, ctx):
        return self.server.get_member(ctx.author.id)

    def get_role(self):
        return self.server.get_role(self.role_id)

    def get_guild(self):
        return self.guild_id