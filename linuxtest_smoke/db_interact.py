# this is used for INSERT, ALTER, etc
# CALLABLE: db_interact(my_stmt)
# CALLED BY: 
# input: a non-SELECT statement (my_stmt)
# return: 
def db_interact(my_stmt):
  print("DEBUG: db_interact(my_stmt) got: " + my_stmt)
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
    cnx.commit()
    cursor.close()
    cnx.close()
    #print("DEBUG: returning 1")
    # 1 is successful
    return 1
  #print("DEBUG: did db_execute(my_stmt) lol")
