# works as intended
import mysql.connector
from mysql.connector import errorcode

def db_try_connect():
  try:
    cnx = mysql.connector.connect(user='root', password='nice_password',
                                  host='127.0.0.1', database='linuxquiztest')
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
  #else:
  else:
    return(cnx)
    #cnx.close()
