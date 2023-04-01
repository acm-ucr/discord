import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class Sendgrid:

    def __init__(self):
        load_dotenv()
        SG_API_KEY = os.getenv('SENDGRID_API_KEY')
        self.sendgrid = SendGridAPIClient(SG_API_KEY)

    def sendEmail(self, email, name, discord, uuid):
        message = Mail(from_email='contact.acmucr@gmail.com',
                       to_emails=email,
                       subject='ACM UCR Discord Verification',
                       html_content=self.generateMessage(uuid, name, discord))

        try:
            self.sendgrid.send(message)
        except Exception as e:
            print(e)

    def generateMessage(self, uuid, name, discord):
        html_message = f"""
        Hello <b>{name}</b>,
        <br/><br/>
        This is a verification email from ACM at UCR to verify your Discord account within the ACM at UCR Discord Server. The Discord account, <b>{discord}</b>, will be connected to this email and used for the verification process. Please use the following code to verify your account:
        <br/><br/>
        Verification Code: <b>{uuid}</b>
        <br/><br/>
        If this is not the correct email and discord association, please contact an ACM officer immediately. You can contact us at acm@cs.ucr.edu. 
        <br/><br/>
        Thank you
        ACM at UCR

        """

        return html_message
