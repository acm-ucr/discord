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

    def getUser(self, discord):
        query_ref = self.db_ref.where(u'discord', u'==', discord).limit(1)

        docs = query_ref.get()

        for doc in docs:
            return doc.id, doc.to_dict()
        return ("", {})

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
        query_ref = self.db_ref.where(u'discord', u'==', discord).limit(1)

        docs = query_ref.get()

        for doc in docs:
            user = {"id": doc.id, "data": doc.to_dict()}

        if user["data"]["uuid"] == uuid:
            self.db_ref.document(user["id"]).update({
                'verified':
                True,
                "verified_at":
                datetime.now()
            })
            return True
        return False

    # def updateEmail(self, discord, email):
    #     query_ref = self.db_ref.where(u'discord', u'==', discord).limit(1)

    #     docs = query_ref.get()

    #     for doc in docs:
    #         user = {"id": doc.id, "data": doc.to_dict()}

    #     self.db_ref.document(user["id"]).update({'email': email})
