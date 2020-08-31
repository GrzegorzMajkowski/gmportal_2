from the_app._database.connection_pool import pool
import the_app._database.database_bank


def add_new_customer(first_name,last_name,email,address,city,birth_date):
    connection = pool.getconn()
    cust_num=the_app._database.database_bank.add_customer(connection=connection,
                                                            first_name=first_name,
                                                            last_name=last_name,
                                                            birthdate_input=birth_date,
                                                            email=email,
                                                            address=address,
                                                            city=city)
    pool.putconn(connection)
    return cust_num

def get_customer(cust_num):
    connection = pool.getconn()
    customer = the_app._database.database_bank.get_customer(connection=connection,customer_number=cust_num)
    pool.putconn(connection)
    return customer

def update_customer(cust_num,first_name,last_name,email,address,city,birth_date):
    connection = pool.getconn()
    the_app._database.database_bank.update_customer(connection=connection,
                                    cust_num=cust_num,
                                    first_name=first_name,
                                    last_name=last_name,
                                    email=email,
                                    address=address,
                                    city=city,
                                    birth_date=birth_date
                                                                )
    pool.putconn(connection)

def get_all_customers():
    connection=pool.getconn()
    customers = the_app._database.database_bank.get_all_customres(connection)
    pool.putconn(connection)
    return customers

def get_customers_by_name(name):
    connection=pool.getconn()
    customers = the_app._database.database_bank.get_customers_by_name(connection, name)
    pool.putconn(connection)
    return customers

def get_accounts(cust_num):
    connection = pool.getconn()
    accounts = the_app._database.database_bank.get_accounts(connection,cust_num)
    pool.putconn(connection)
    return accounts

def get_account(account_num):
    connection = pool.getconn()
    account = the_app._database.database_bank.get_account(connection,account_num)
    pool.putconn(connection)
    return account

def get_last_transactions(account_num):
    connection = pool.getconn()
    account = the_app._database.database_bank.get_last_transactions(connection,account_num)
    pool.putconn(connection)
    return account

def add_new_account(customer_num,account_name):
    connection = pool.getconn()
    account = the_app._database.database_bank.add_new_account(connection,customer_num,account_name)
    pool.putconn(connection)


def make_transaction(account_in,account_out, quote,trans_type,trans_title):
    connection = pool.getconn()
    message = the_app._database.database_bank.db_transaction(connection,account_in,account_out, quote,trans_type,trans_title)
    pool.putconn(connection)
    return message

    
def get_transaction_details(transaction_num):
    connection = pool.getconn()
    transactions = the_app._database.database_bank.get_transaction_details(connection,transaction_num)
    pool.putconn(connection)
    return transactions

