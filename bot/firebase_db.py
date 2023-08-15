import os
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dotenv import load_dotenv

class Firestore:
    """Wrapper class for interacting with Firestore database."""

    def __init__(self):
        """Initialize Firestore connection and reference."""
        load_dotenv()
        CREDS = os.getenv("CREDS")

        with open("firebase_creds.json", "w", encoding="utf-8") as file:
            file.write(CREDS)

        cred: credentials.Certificate = credentials.Certificate("firebase_creds.json")
        firebase_admin.initialize_app(cred)

        db: firestore.Firestore = firestore.client()
        self.db_ref: firestore.AsyncCollectionReference = db.collection('users')

    def getUser(self, discord, email):
        """Fetch user information based on Discord ID or email.

        Args:
            discord (str): Discord ID.
            email (str): User's email.

        Returns:
            list: A list containing the user's ID and data if found, or an error message.
        """
        query_ref: Query = self.db_ref.where('discord', '==', discord)
        discord_docs: list = query_ref.get()

        query_ref: Query = self.db_ref.where('email', '==', email)
        email_docs: list = query_ref.get()

        if len(discord_docs) == 0 and len(email_docs) == 0:
            return ["", {}]

        if len(discord_docs) != 1 and len(email_docs) != 1:
            return ["Too Many or Not Enough Documents Fetched", {}]

        discord_id: str = ""
        email_id: str = ""
        discord_doc: dict = None

        for doc in discord_docs:
            discord_id: str = doc.id
            discord_doc: dict = doc.to_dict()
        for doc in email_docs:
            email_id: str = doc.id

        if discord_id == email_id:
            return [discord_id, discord_doc]
        return ["Too Many or Not Enough Documents Fetched", {}]

    #pylint: disable-msg=too-many-arguments
    def createUser(self, email, name, discord, uuid, affiliation):
        """Create a new user and add their data to the Firestore database.

        Args:
            email (str): User's email.
            name (str): User's name.
            discord (str): Discord ID.
            uuid (str): User's UUID.
            affiliation (str): User's affiliation.
        """
        data: dict = {
            "email": email,
            "name": name,
            "discord": discord,
            "uuid": uuid,
            "affiliation": affiliation,
            "verified": False,
            "created_at": datetime.now()
        }

        self.db_ref.add(data)

    #pylint: enable-msg=too-many-arguments

    def verifyUser(self, discord, uuid):
        """Verify a user based on their Discord ID and UUID.

        Args:
            discord (str): Discord ID.
            uuid (str): User's UUID.

        Returns:
            list: A list containing True if the user is verified, along with user data, or False if not verified.
        """
        query_ref: Query = self.db_ref.where('discord', '==', discord)
        docs: list = query_ref.get()

        if len(docs) != 1:
            return [False, {
                "error": "Too Many or Not Enough Documents Fetched"
            }]

        for doc in docs:
            user: dict = {"id": doc.id, "data": doc.to_dict()}

        if user["data"]["uuid"] == uuid:
            self.db_ref.document(user["id"]).update({
                'verified':
                True,
                "verified_at":
                datetime.now()
            })
            return [True, user["data"]]
        return [False, {}]

    # def updateEmail(self, discord, email):
    #     query_ref = self.db_ref.where(u'discord', u'==', discord).limit(1)

    #     docs = query_ref.get()

    #     for doc in docs:
    #         user = {"id": doc.id, "data": doc.to_dict()}

    #     self.db_ref.document(user["id"]).update({'email': email})
