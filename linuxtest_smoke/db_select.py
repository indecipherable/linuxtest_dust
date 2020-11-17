# imports
import mysql.connector
from mysql.connector import errorcode
# CALLABLE: db_execute(my_stmt)
# CALLED BY: show_options()
# input: a SELECT statement (my_stmt)
# return: 
def db_select(my_stmt):
  my_rows=''
  line_ct=int(0)
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
  else:
    cursor = cnx.cursor()
    cursor.execute(my_stmt,params=None,multi=False)
    my_rows = cursor.fetchall()
    cursor.close()
    cnx.close()
    for line in my_rows:
      line_ct=line_ct+1
  return(line_ct,my_rows)
