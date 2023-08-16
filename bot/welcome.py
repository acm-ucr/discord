"""Send welcome messages when a member joins the server"""

from discord import Embed, Member, Color

# pylint: disable=too-few-public-methods
class Welcome:
    """Class to Handle Welcome Events"""

    def __init__(self):
        pass

    async def send_welcome_message(self, member: Member):
        """Send welcome message to new members in server"""
        embed: Embed = Embed(
            title="Welcome to ACM!",
            description=
            "To gain access to the full server, please run the following slash commands.",
            color=Color.blue())
        embed.add_field(name="/verify",
                        value="You will receive an 8-digit code in your email",
                        inline=False)
        embed.add_field(
            name="/code",
            value="Please enter that code in this command for verification",
            inline=True)

        await member.send(embed=embed)
