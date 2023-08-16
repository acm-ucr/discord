import os
from datetime import datetime
from firebase_admin import firestore, initialize_app, credentials, Query
from dotenv import load_dotenv

class Firestore:
    """Wrapper class for interacting with Firestore database"""

    def __init__(self):
        """Initialize Firestore connection and reference."""
        load_dotenv()
        CREDS = os.getenv("CREDS")

        with open("firebase_creds.json", "w", encoding="utf-8") as file:
            file.write(CREDS)

        cred: credentials.Certificate = credentials.Certificate("firebase_creds.json")
        initialize_app(cred)

        db: firestore.Firestore = firestore.client()
        self.db_ref: firestore.AsyncCollectionReference = db.collection('users')

    def getUser(self, discord, email):
        """Fetch user information based on Discord ID or email"""
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
        """Create a new user and add their data to the Firestore database"""
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

    def verifyUser(self, discord, uuid):
        """Verify a user based on their Discord ID and UUID"""
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