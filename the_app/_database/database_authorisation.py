import datetime


#**********************************************************************
# Adding new user
#**********************************************************************
ADD_NEW_USER = """
    INSERT INTO users (email, username, password_hash) VALUES (%s,%s,%s);
;"""

def add_new_user(connection,email:str, username:str, password_hash:str):
    with connection:
        cur=connection.cursor()
        cur.execute(ADD_NEW_USER,(email,username, password_hash))

def check_email_exixts(connection, email):
    with connection:
        cur=connection.cursor()
        cur.execute("SELECT id FROM users WHERE email = %s",(email,))
        check_data= cur.fetchone()
        if check_data:
            return True
        else:
            return False

def check_username_exixts(connection, username):
    with connection:
        cur=connection.cursor()
        cur.execute("SELECT id FROM users WHERE username = %s",(username,))
        check_data= cur.fetchone()
        if check_data:
            return True
        else:
            return False
#**********************************************************************


#**********************************************************************
# Login user
#**********************************************************************
def search_for_user(connection,email):
    with connection:
        cur=connection.cursor()
        cur.execute("SELECT id, email, username, role, password_hash FROM users WHERE email = %s",(email,))
        user = cur.fetchone()
        if user:
            return user
        else:
            return None



ADD_LOGLOGIN = """  
    INSERT INTO loglogin (user_id, user_email, user_username, user_role, user_agent, user_remote_adr ) VALUES (%s,%s,%s,%s,%s,%s)
;"""

def log_login(connection, id, email, username, role, agent, remote_adr):
    with connection:
        cur=connection.cursor()
        cur.execute(ADD_LOGLOGIN,(id,email,username,role,agent,remote_adr))
#**********************************************************************

