# works as intended
import mysql.connector
from mysql.connector import errorcode


def main():
  operation="SHOW TABLES;"
  #operation="SELECT * from questions;"
  try:
    cnx = mysql.connector.connect(user='root', password='nice_password',
                                  host='127.0.0.1', database='linuxquiztest')
    cursor = cnx.cursor()
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
  else:
    cursor.execute(operation, params=None, multi=False)
    tables = cursor.fetchall()
    for a_table in tables:
      print(a_table[0])
    cursor.close()
  return tables

main()
