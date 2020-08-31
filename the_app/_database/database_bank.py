import datetime


ADD_CUSTOMER = """
    INSERT INTO customers (first_name, last_name, email, address, city, birth_date_text, birth_date_date) VALUES (%s,%s,%s,%s,%s, %s, %s) RETURNING id;
"""
UPDATE_CUSTOMER_NUMBER = """
    UPDATE customers SET customer_number = %s WHERE id = %s;
"""

def add_customer(connection,first_name:str, last_name:str, birthdate_input:str,email:str, address:str, city:str):
    #birthdate_date_ = datetime.datetime.strptime(birthdate_input, "%Y-%m-%d")

    with connection:
        cur=connection.cursor()
        cur.execute(ADD_CUSTOMER,(first_name,last_name, email,address,city,birthdate_input,birthdate_input))
        last_id = cur.fetchone()[0]
        cust_num = 5000+last_id
        cur.execute(UPDATE_CUSTOMER_NUMBER,(cust_num,last_id))
        return cust_num

SELECT_CUSTOMER = """
    SELECT * FROM customers WHERE customer_number = %s;
"""

def get_customer(connection,customer_number):
    with connection:
        cur=connection.cursor()
        cur.execute(SELECT_CUSTOMER,(customer_number,))
        return cur.fetchone()



UPDATE_CUSTOMER = """
    UPDATE customers SET first_name=%s, last_name=%s, email=%s, address=%s , city=%s, birth_date_date = %s WHERE customer_number = %s
"""
def update_customer(connection,cust_num, first_name,last_name,email,address,city,birth_date):
    with connection:
        cur=connection.cursor()
        cur.execute(UPDATE_CUSTOMER,(first_name,last_name,email,address,city,birth_date,cust_num))

SELECT_ALL_CUSTOMERS = """
    SELECT customer_number, first_name, last_name, email, address, city, birth_date_date FROM customers ORDER BY last_name ASC;
"""
def get_all_customres(connection):
    with connection:
        cur=connection.cursor()
        cur.execute(SELECT_ALL_CUSTOMERS)
        return cur.fetchall()


SELECT_CUSTOMERS_BY_NAME= """
    SELECT customer_number, first_name, last_name, email, address, city, birth_date_date FROM customers WHERE last_name ILIKE %s ORDER BY last_name ASC;
"""
def get_customers_by_name(connection, name):
    with connection:
        cur=connection.cursor()
        cur.execute(SELECT_CUSTOMERS_BY_NAME, (f"%{name}%",))
        return cur.fetchall()

SELECT_ACCOUNTS_FOR_CUSTOMER= """
    SELECT account_number, name, balance, posting_date FROM accounts WHERE customer_number = %s;
"""
def get_accounts(connection,cust_num):
    with connection:
        cur=connection.cursor()
        cur.execute(SELECT_ACCOUNTS_FOR_CUSTOMER, (cust_num,))
        return cur.fetchall()

SELECT_ACCOUNT= """
    SELECT account_number, name, balance, posting_date, customer_number FROM accounts WHERE account_number = %s;
"""
def get_account(connection,account_num):
    with connection:
        cur=connection.cursor()
        cur.execute(SELECT_ACCOUNT, (account_num,))
        return cur.fetchone()



SELECT_LAST_TRANSACTIONS_FOR_ACCOUNT = """
    SELECT transactions.transaction_number as trans_num,
    transaction_list.posting_date,
    transactions.transaction_type, 
    transactions.transaction_title , 
    transactions.quote, 
    transactions.balance_after_transaction ,
    transactions.account_number
    FROM transaction_list INNER JOIN transactions ON transaction_list.transaction_number = transactions.transaction_number 
    WHERE account_number = %s ORDER BY transactions.id DESC LIMIT 5;
"""


def get_last_transactions(connection,account_num):
    with connection:
        cur=connection.cursor()
        cur.execute(SELECT_LAST_TRANSACTIONS_FOR_ACCOUNT, (account_num,))
        return cur.fetchall()


SELECT_TRANSACTION_DETAILS = """   
    SELECT transactions.transaction_number as trans_num,
    transaction_list.posting_date,
    transactions.transaction_type, 
    transactions.transaction_title , 
    transactions.quote, 
    transactions.balance_after_transaction ,
    transactions.account_number 
    FROM transaction_list INNER JOIN transactions ON transaction_list.transaction_number = transactions.transaction_number 
    WHERE transactions.transaction_number = %s ORDER BY transactions.id DESC LIMIT 5
;"""
def get_transaction_details(connection,transaction_num):
    with connection:
        cur=connection.cursor()
        cur.execute(SELECT_TRANSACTION_DETAILS, (transaction_num,))
        return cur.fetchall()

        

ADD_ACCOUNT= """
    INSERT INTO accounts (name, customer_number,creation_date_timestamp) VALUES (%s,%s,%s) RETURNING id;
"""

UPDATE_ACCOUNT_NUMBER = """
    UPDATE accounts SET account_number = %s WHERE id = %s;
"""

def add_new_account(connection,customer_num,account_name):
    creation_date_timestamp = datetime.datetime.now().timestamp()
    with connection:
        cur=connection.cursor()
        cur.execute(ADD_ACCOUNT, (account_name,customer_num,creation_date_timestamp))
        last_id = cur.fetchone()[0]
        acc_num=9000+last_id
        cur.execute(UPDATE_ACCOUNT_NUMBER, (acc_num,last_id))


def db_transaction(connection, account_in,account_out, quote,trans_type,trans_title):
    with connection:
        cur=connection.cursor()
        cur.execute("SELECT balance FROM accounts WHERE account_number = %s;",(account_out,))
        account_out_balance = cur.fetchone()[0]

        cur.execute("SELECT balance FROM accounts WHERE account_number = %s;",(account_in,))
        account_in_balance = cur.fetchone()[0]

        if  not account_in_balance:
            if account_in_balance != 0.0:
                message = "Zły numer rachunku docelowego. Transakcja nie zrealizowana!"
                category = 'warning'
                return [message, category]

        if not account_out_balance:
            message = "Zły numer rachunku źródłowego. Transakcja nie zrealizowana!"
            category = 'warning'
            return [message, category]




        if account_out_balance < float(quote):
            message = "Ilość środków na koncie nie jest wystarczająca aby przeprowadzić transakcję !!!"
            category = 'warning'
        else:
            message = ("Transacja może być zaakceptowana. \n")
            #input("ENTER aby kontynuowac...")

            
            transaction_date_timestamp = datetime.datetime.now().timestamp()
            transaction_type=trans_type+'_out'
            account_out_new_balance = account_out_balance - float(quote)

            cur.execute("INSERT INTO transaction_list (transaction_number, transaction_date_timestamp) VALUES (0,%s) RETURNING id;",(transaction_date_timestamp,))
            last_id = cur.fetchone()[0]
            trans_num=7000+last_id
            cur.execute("UPDATE transaction_list SET transaction_number = %s WHERE id = %s;", (trans_num,last_id))

            cur.execute("UPDATE accounts SET balance = %s WHERE account_number = %s;",(account_out_new_balance,account_out))
            cur.execute("INSERT INTO transactions (transaction_number, account_number, transaction_type, quote, balance_after_transaction, transaction_title) VALUES (%s,%s,%s,%s,%s,%s);", (trans_num, account_out,transaction_type,'-'+quote,account_out_new_balance,trans_title ))
            message += (f"  --> Kwota -{quote} z rachunku {account_out}.\n")

            transaction_type=trans_type+'_in'
            account_in_new_balance = account_in_balance + float(quote)
            cur.execute("UPDATE accounts SET balance = %s WHERE account_number = %s;",(account_in_new_balance,account_in))
            cur.execute("INSERT INTO transactions (transaction_number, account_number, transaction_type, quote, balance_after_transaction, transaction_title) VALUES (%s,%s,%s,%s,%s,%s);", (trans_num, account_in,transaction_type,quote,account_in_new_balance,trans_title ))
            message += (f"  --> Kwota +{quote} na rachunek {account_in}.\n")
            category='success'

        return [message, category]


