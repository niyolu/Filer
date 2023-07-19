from sqlalchemy import create_engine

# CONN_STR = "mysql+pymysql://root:pw@localhost/db?host=localhost?port=3306"


user = "root"
pw = "my-secret-pw"
host = "localhost"
port = "3306"
database = "db"

CONN_STR = f"mysql+mysqlconnector://{user}:{pw}@{host}:{port}/{database}"
#CONN_STR = "jdbc+mysql://root@localhost:3306/"

engine = create_engine(CONN_STR)
conn = engine.connect()

# Access denied for user 'root'@'172.23.0.1' (using password: YES)

print(conn.execute("SELECT host FROM INFORMATION_SCHEMA.PROCESSLIST WHERE ID = CONNECTION_ID()").fetchall())



# # from sqlalchemy import create_engine
# # from sqlalchemy.orm import sessionmaker

# # # from app.core.config import settings

# # engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
# # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# import mysql.connector

# cnx = mysql.connector.connect(user='user', password='my-secret-pw',
# host='localhost',
# database='db')
# cnx.close()

# import mysql.connector as mysql

# def main():
#     cnx = mysql.connect(
#         user='user', 
#         password='pw', 
#         database='mysql',
#         host='localhost', 
#         port=3306
#     )
#     cursor = cnx.cursor()

#     cursor.execute("CREATE TABLE IF NOT EXISTS test(id INTEGER(64) PRIMARY KEY, name VARCHAR(255))")

#     cursor.execute("INSERT INTO test VALUES (2, 'bla')")
#     cursor.execute("INSERT INTO test VALUES (3, 'blabla')")
#     cursor.execute("INSERT INTO test VALUES (4, 'blablabla')")

#     cursor.execute("SELECT * FROM test")
#     for row in cursor.fetchall():
#         print(row)
    
#     cursor.close()
#     cnx.close()

# if __name__ == "__main__":
#     main()