from werkzeug.security import generate_password_hash, check_password_hash
from the_app._database.connection_pool import pool
import the_app._database.database_authorisation

class NewUser():
    # overall_result=False
    # email_exists=False
    # username_exists=False

    def __init__(self, overall_result, email_exists, username_exists):
        self.overall_result=overall_result
        self.email_exists=email_exists
        self.username_exists=username_exists



def addNewUser(email, username, password):

    newUserCheck= NewUser(False,False,False)

    connection = pool.getconn()

    newUserCheck.email_exists = the_app._database.database_authorisation.check_email_exixts(connection,email)
    newUserCheck.username_exists = the_app._database.database_authorisation.check_username_exixts(connection,username)
    
    newUserCheck.overall_result=1
    if (newUserCheck.email_exists) or (newUserCheck.username_exists):
        newUserCheck.overall_result=False
    else:
        newUserCheck.overall_result=True
        password_hash= generate_password_hash(password)
        the_app._database.database_authorisation.add_new_user(connection,email,username,password_hash)

    pool.putconn(connection)
    return newUserCheck


def authenticate_user(email,password,user_remote_addr,user_agent):

    connection = pool.getconn()
    user = the_app._database.database_authorisation.search_for_user(connection,email)
    if user is not None and check_password_hash(user[4],password):
        the_app._database.database_authorisation.log_login(connection, id=user[0], email=user[1], username=user[2], role=user[3], agent=user_agent, remote_adr=user_remote_addr)
        pool.putconn(connection)
        return user
    else:
        pool.putconn(connection)
        return None

def loader_user(email):
    connection = pool.getconn()
    user = the_app._database.database_authorisation.search_for_user(connection,email)
    pool.putconn(connection)

    if user is not None:
        return user
    else:
        return None

