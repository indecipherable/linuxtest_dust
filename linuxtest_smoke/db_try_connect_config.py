# works as intended
import mysql.connector
from mysql.connector import errorcode

config = {
  'user': 'root',
  'password': 'nice_password',
  'host': '127.0.0.1',
  'database': 'linuxquiztest',
  'raise_on_warnings': True,
  'use_pure': False
}

def main():
  try:
    cnx = mysql.connector.connect(**config)
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
  else:
    stmt = "SHOW databases;"
    cursor = cnx.cursor()
    cursor.execute(stmt, params=None, multi=False)
    databases = cursor.fetchall()
    for a_database in databases:
      print(a_database)
    cursor.close()
    cnx.close()
    return databases

main()
