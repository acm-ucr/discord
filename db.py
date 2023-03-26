import psycopg2
import os
from dotenv import load_dotenv


def createConnection():
    load_dotenv()
    host = os.getenv('POSTGRES_HOST')
    database = os.getenv('POSTGRES_DATABASE')
    username = os.getenv('POSTGRES_USERNAME')
    pwd = os.getenv('POSTGRES_PASSWORD')
    port = os.getenv('POSTGRES_PORT')

    try:
        connection = psycopg2.connect(
                host=host,
                dbname=database,
                user=username,
                password=pwd,
                port=port
            )
        cursor = connection.cursor()
    except Exception as error:
        print(error)
        return None, None

    return connection, cursor

def getUser(email, discordID):
    connection, cursor = createConnection()

    if connection and cursor:
        get_user = f"SELECT * FROM emailverification.user WHERE email='{email}' OR discordid='{discordID}'"
        cursor.execute(get_user)
        result = cursor.fetchall()[0]

        connection.close()
        cursor.close()
   
    return result


def createUser(email, name, discordID, uuid):
    connection, cursor = createConnection()

    if connection and cursor:
        create_user = f"INSERT INTO emailverification.user(name, email, code, discordid, verified) VALUES({name}, {email}, {uuid}, {discordID}, False)"
        cursor.execute(create_user)
        connection.commit()

        connection.close()
        cursor.close()


def verifyUser(discordID, uuid):
    connection, cursor = createConnection()
    verified = False

    if connection and cursor:
        verify_user = f"SELECT * FROM emailverification.user WHERE discordid='{discordID}'"
        cursor.execute(verify_user)

        result = cursor.fetchall()[0]
        
        if(result[2] == uuid):
            verify = f"UPDATE emailVerification.user SET verified='True' WHERE discordid='{discordID}'"
            cursor.execute(verify)
            connection.commit()
            verified = True

        connection.close()
        cursor.close()

    return verified


def updateEmail(discordID, email):
    connection, cursor = createConnection()

    if connection and cursor:
        update_email = f"UPDATE emailVerification.user SET email='{email}' WHERE discordid='{discordID}'"
        cursor.execute(update_email)
        connection.commit()
    
        connection.close()
        cursor.close()