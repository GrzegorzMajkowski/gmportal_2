import os
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv


load_dotenv()
database_uri = os.environ["DATABASE_URI"]


# def create_connection():
#     return psycopg2.connect(os.environ.get("DATABASE_URI"))

pool = SimpleConnectionPool(minconn=1,maxconn=5, dsn=database_uri)

# @contextmanager
# def get_connection():
#     connection = pool.getconn()

#     try:
#         yield connection
#     finally:
#         pool.putconn(connection)