import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dotenv import load_dotenv
from datetime import datetime


class Firestore:

    def __init__(self):
        load_dotenv()
        CREDS = os.getenv("CREDS")

        with open("firebase_creds.json", "w") as file:
            file.write(CREDS)

        cred = credentials.Certificate("firebase_creds.json")
        firebase_admin.initialize_app(cred)

        db = firestore.client()
        self.db_ref = db.collection(u'users')

    def getUser(self, discord, email):
        query_ref = self.db_ref.where(u'discord', u'==', discord)
        discord_docs = query_ref.get()

        query_ref = self.db_ref.where(u'email', u'==', email)
        email_docs = query_ref.get()

        if len(discord_docs) == 0 and len(email_docs) == 0:
            return ("", {})

        if len(discord_docs) != 1 and len(email_docs) != 1:
            return ("Too Many or Not Enough Documents Fetched", {})

        discord_id, email_id = "", ""
        discord_doc = None

        for doc in discord_docs:
            discord_id = doc.id
            discord_doc = doc.to_dict()
        for doc in email_docs:
            email_id = doc.id

        if discord_id == email_id:
            return (discord_id, discord_doc)
        else:
            return ("Too Many or Not Enough Documents Fetched", {})

    def createUser(self, email, name, discord, uuid, affiliation):
        data = {
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
        query_ref = self.db_ref.where(u'discord', u'==', discord)
        docs = query_ref.get()

        if len(docs) != 1:
            return (False, {"error": "Too Many or Not Enough Documents Fetched"})

        for doc in docs:
            user = {"id": doc.id, "data": doc.to_dict()}

        if user["data"]["uuid"] == uuid:
            self.db_ref.document(user["id"]).update({
                'verified':
                True,
                "verified_at":
                datetime.now()
            })
            return (True, user["data"])
        return (False, {})

    # def updateEmail(self, discord, email):
    #     query_ref = self.db_ref.where(u'discord', u'==', discord).limit(1)

    #     docs = query_ref.get()

    #     for doc in docs:
    #         user = {"id": doc.id, "data": doc.to_dict()}

    #     self.db_ref.document(user["id"]).update({'email': email})