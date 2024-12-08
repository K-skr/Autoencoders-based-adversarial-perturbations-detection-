from database import db

def runQuery(q):
    try:
        cursor = db.cursor()
        cursor.execute(q)
        if q.strip().upper().startswith("INSERT") or q.strip().upper().startswith("UPDATE") or q.strip().upper().startswith("DELETE"):
            db.commit()
            rows = cursor.fetchall()
            cursor.close()
            return rows
        elif q.strip().upper().startswith("SELECT"):
            rows = cursor.fetchall()
            cursor.close()
            return rows
        return []
    except Exception as e:
        print("Error executing Query  : "+q)
        print(e)

def createUser(email,password):
    if userExists(email):
        return False
    runQuery(f"INSERT INTO USER(email,password) VALUES('{email}','{password}')")
    rows = runQuery(f"SELECT id FROM USER WHERE EMAIL='{email}'")
    
    if rows == None:
        return False
    
    return rows[0]

def userExists(email):
    rows = runQuery(f"SELECT email FROM USER WHERE email='{email}'")
    # print(rows)
    if(rows==None or len(rows)==0):
        return False
    else:
        return True

def checkForValidLogin(email,password):
    rows = runQuery(f"SELECT id FROM USER WHERE email='{email}' AND password='{password}'")
    # print(rows)
    if(rows==None or len(rows)==0):
        return False
    else:
        return rows[0]