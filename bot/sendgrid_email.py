import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, SendGridException

class Sendgrid:
    """Wrapper class for sending emails using the SendGrid API."""

    def __init__(self):
        """Initialize the Sendgrid client using the API key from environment variables."""
        load_dotenv()
        SG_API_KEY = os.getenv('SENDGRID_API_KEY')
        self.sendgrid: SendGridAPIClient = SendGridAPIClient(SG_API_KEY)

    def sendEmail(self, email, name, discord, uuid):
        """Send an email with verification information.

        Args:
            email (str): Recipient's email address.
            name (str): Recipient's name.
            discord (str): Recipient's Discord ID.
            uuid (str): Verification UUID.
        """
        message: dict = Mail(from_email='contact.acmucr@gmail.com',
                             to_emails=email,
                             subject='ACM UCR Discord Verification',
                             html_content=self.generateMessage(uuid, name, discord))

        try:
            self.sendgrid.send(message)
        except SendGridException as e:
            print(f"An error occurred while sending the email: {str(e)}")

    def generateMessage(self, uuid, name, discord):
        """Generate the HTML content for the verification email.

        Args:
            uuid (str): Verification UUID.
            name (str): Recipient's name.
            discord (str): Recipient's Discord ID.

        Returns:
            str: HTML content for the verification email.
        """
        html_message: str = f"""
        Hello <b>{name}</b>,
        <br/><br/>
        This is a verification email from ACM at UCR to verify your Discord account within the ACM at UCR Discord Server. The Discord account, <b>{discord}</b>, will be connected to this email and used for the verification process. Please use the following code to verify your account:
        <br/><br/>
        Verification Code: <b>{uuid}</b>
        <br/><br/>
        If this is not the correct email and discord association, please contact an ACM officer immediately. You can contact us at acm@cs.ucr.edu. 
        <br/><br/>
        Thank you<br/>
        ACM at UCR

        """

        return html_message
