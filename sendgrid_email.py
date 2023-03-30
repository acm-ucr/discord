import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class Sendgrid:

    def __init__(self):
        load_dotenv()
        SG_API_KEY = os.getenv('SENDGRID_API_KEY')
        self.sendgrid = SendGridAPIClient(SG_API_KEY)

    def sendEmail(self, email, uuid):
        message = Mail(from_email='contact.acmucr@gmail.com',
                       to_emails=email,
                       subject='ACM UCR Discord Verification',
                       plain_text_content=f'Here is your code {uuid}')

        try:
            self.sendgrid.send(message)
        except Exception as e:
            print(e)
