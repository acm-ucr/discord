"""
OS:
    getenv function used to access Firebase credentials

dotenv:
    load_dotenv function loads environment variables

datetime:
    datetime module used to record creation date of user entries in database

firebase_admin:
    module used to initialize database application with credentials

firebase_admin:
    credentials module used to certificate Firebase credentials

    firestore module used to create client for communication with database
"""
import os
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dotenv import load_dotenv


class Firestore:

    """
    A class used to manage Firebase database
    ...
    Attributes
    ----------
    db_ref: The reference to the collection of users in the database

    Methods
    -------
    getUser(discord, email)
        Searches the database for the user with values matching the parameters
        Returns the found user document 
    
    createUser(email, name, discord, uuid, affiliation):
        Updates the database with a new user document containing the parameters as the values

    verifyUser(discord, uuid):
        Checks whether the provided uuid code matches the one stored in the user document 
        Returns a boolean based on the check 
        Returns a reference to that user document if the check passed
    """

    def __init__(self):
        """
        Initiliazes the Firebase application with the credentials
        """
        load_dotenv()
        CREDS = os.getenv("CREDS")

        with open("firebase_creds.json", "w", encoding="utf-8") as file:
            file.write(CREDS)

        cred = credentials.Certificate("firebase_creds.json")
        firebase_admin.initialize_app(cred)

        db = firestore.client()
        self.db_ref = db.collection('users')

    def getUser(self, discord, email):
        """
        Gets the user from the database based on the two values provided

        Parameters
        ----------
        email : str
            The desired user's email
        discord : str
            The desired user's discord tag
        
        Return
        ----------
        returns the user document if found, 
        else returns a not found message

        """
        query_ref = self.db_ref.where('discord', '==', discord)
        discord_docs = query_ref.get()

        query_ref = self.db_ref.where('email', '==', email)
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
        return ("Too Many or Not Enough Documents Fetched", {})
    #pylint: disable-msg=too-many-arguments
    def createUser(self, email, name, discord, uuid, affiliation):
        """
        Creates the user from the database based on the provided values

        Parameters
        ----------
        email : str
            The user's email address
        name : str
            The user's name
        discord : str
            The user's discord tag
        uuid: str
            The verification code to verify the user with
        affiliation: str
            The user's affiliation

        """
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
    #pylint: enable-msg=too-many-arguments

    def verifyUser(self, discord, uuid):
        """
        Verifies the user from the database has the same code as the one provided to the bot

        Parameters
        ----------
        discord : str
            The desired user's discord tag
        uuid: str
            The verification code to verify the user with
        Return
        ----------
        Returns a boolean based on the verification success
        Returns a reference to that user document if the verification passed

        """
        query_ref = self.db_ref.where('discord', '==', discord)
        docs = query_ref.get()

        if len(docs) != 1:
            return (False, {
                "error": "Too Many or Not Enough Documents Fetched"
            })

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
