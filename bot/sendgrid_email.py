"""
OS:
    getenv function used to access Sendgrid API Key

dotenv:
    load_dotenv function loads environment variables

sendgrid:
    SendGridAPIClient function forms the API connection with the API Key

sendgrid.helpers.mail:
    Mail function sends emails through the API connection

    SendGridException covers exceptions specifically related to the SendGrid API
"""
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, SendGridException


class Sendgrid:
    """
    A class used to manage sending emails

    ...

    Attributes
    ----------
    sendgrid: The sendgrid API connection

    Methods
    -------
    sendEmail(email, name, discord, uuid)
        Sends the email generated with the name, discord, and uuid to the desired email address 
    
    generateMessage(uuid, name, discord):
        Utilizes a format to generate an email to send using the uuid, name, and discord
    """

    def __init__(self):
        """
        Initiliazes the sendgrid API connection using the API key
        """

        load_dotenv()
        SG_API_KEY = os.getenv('SENDGRID_API_KEY')
        self.sendgrid = SendGridAPIClient(SG_API_KEY)

    def sendEmail(self, email, name, discord, uuid):
        """
        Sends an email to the user we want to verify to inform them of the verification code

        Parameters
        ----------
        email : str
            The email to send to
        name : str
            The name of the user to verify
        discord : str
            The discord tag of the user to verify
        uuid: str
            The verification code to verify the user with
        """
        message = Mail(from_email='contact.acmucr@gmail.com',
                       to_emails=email,
                       subject='ACM UCR Discord Verification',
                       html_content=self.generateMessage(uuid, name, discord))

        try:
            self.sendgrid.send(message)
        except SendGridException as e:
            print(f"An error occurred while sending the email: {str(e)}")

    def generateMessage(self, uuid, name, discord):
        """
        Generates an email to inform the user of the verification code
        
        Parameters
        ----------
        name : str
            The name of the user to verify
        discord : str
            The discord tag of the user to verify
        uuid: str
            The verification code to verify the user with
        """
        html_message = f"""
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
