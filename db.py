import psycopg2

host = '35.233.153.157'
database = 'emailVerification'
username = 'postgres'
pwd = '+98U=n"ta=;>x)gS'
port = '5432'
connection = None
cursor = None


def getUser(email, name, discordID):
    result = None
    try:
        connection = psycopg2.connect(
            host=host,
            dbname=database,
            user=username,
            password=pwd,
            port=port
        )
        cursor = connection.cursor()

        getUser = "select * from emailverification.user where email = '" + \
            email+"' or discordid = '"+discordID+"';"

        cursor.execute(getUser)
        for record in cursor.fetchall():
            result = record

        if(connection != None):
            connection.close()
        if(cursor):
            cursor.close()
    except Exception as error:
        print(error)
    # print(result)
    return result


def createUser(email, name, discordID, uuid):
    try:
        connection = psycopg2.connect(
            host=host,
            dbname=database,
            user=username,
            password=pwd,
            port=port
        )
        cursor = connection.cursor()

        createuserScript = "INSERT INTO emailverification.user(name, email, code, discordid, verified) values('" + \
            name+"', '"+email+"', '"+uuid+"', '"+discordID+"', False);"

        cursor.execute(createuserScript)
        connection.commit()

        if(connection != None):
            connection.close()
        if(cursor):
            cursor.close()
    except Exception as error:
        print(error)


def verifyUser(discordID, uuid):
    verified = False
    result = None
    try:
        connection = psycopg2.connect(
            host=host,
            dbname=database,
            user=username,
            password=pwd,
            port=port
        )
        cursor = connection.cursor()

        verifyUserScript = "select * from emailverification.user where discordid = '"+discordID+"';"

        cursor.execute(verifyUserScript)

        for record in cursor.fetchall():
            result = record
        if(result[2] == uuid):
            verifiedScript = "update emailVerification.user set verified = true where discordid = '"+discordID+"';"
            cursor.execute(verifiedScript)
            connection.commit()
            verified = True
        if(connection != None):
            connection.close()
        if(cursor):
            cursor.close()
    except Exception as error:
        print(error)
    return verified


def updateEmail(discordID, email):
    verified = False
    result = None
    try:
        connection = psycopg2.connect(
            host=host,
            dbname=database,
            user=username,
            password=pwd,
            port=port
        )
        cursor = connection.cursor()

        updateEmailScript = "update emailVerification.user set email = '" + \
            email+"' where discordid = '"+discordID+"';"

        cursor.execute(updateEmailScript)
        connection.commit()
        if(connection != None):
            connection.close()
        if(cursor):
            cursor.close()
    except Exception as error:
        print(error)
    return verified