# this methodology for opening and closing database connections
# results in unstable database connection
#
# it's better to open and close the database connection within
# a continuous method

### DB METHODS ###
#  
# CALLABLE:
# CALLED BY show_options()
# input:
# return:
# called by: show_options
def db_cnx_open():
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
    print("DEBUG: cnx.cursor() type:")
    print(type(cursor))
    return(cursor)
# CALLABLE:
# CALLED BY: show_options()
# input:
# return:
def db_cnx_commit():
  print("DEBUG: use db_cnx_commit(cursor,my_id,my_stmt)")
#
# CALLABLE:
# CALLED BY: show_options()
# input:
# return:
def db_cnx_commit(cursor,my_id,my_stmt):
  cursor.execute(my_stmt, params=None, multi=False)
  #iterator = cursor.execute(my_stmt, params=None, multi=True)
  #cursor.execute(my_stmt, params=None, multi=True)
  #cursor.execute(my_stmt, my_data)
  cnx.commit()
  cursor.close()
#
# CALLABLE:
# CALLED BY: show_options()
# input:
# return:
def db_cnx_close():
  print("DEBUG: use db_cursor_execute(my_id,my_stmt)")
#
# CALLABLE:
# CALLED BY: show_options()
# input:
# return:
def db_cnx_close(cursor):
  #cursor.execute("INSERT INTO [table] (%s %s)")
  #my_columns = cursor.fetchall()
  #my_stmt = "INSERT INTO section (......) VALUES (......)"
  #my_data = ["3", 'Is the sky green', 'no', 'yes']
  #my_stmt = "INSERT INTO sections (q_id, section, answer, wrong) VALUES (%s, %s, %s, %s)"
  #print("database_insert.DEBUG: my_stmt is: %r" % my_stmt)
  #print("database_insert.DEBUG: my_data is: %r" % my_data)
  #print("database_insert.DEBUG: Trying to cursor.execute() ....")
  cnx.close()
