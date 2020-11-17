# untested - not sure if this works as intended
def database_insert(my_stmt):
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
    #cursor.execute("INSERT INTO [table] (%s %s)")
    #my_columns = cursor.fetchall()
    #my_stmt = "INSERT INTO question (......) VALUES (......)"
    #my_data = ["3", 'Is the sky green', 'no', 'yes']
    #my_stmt = "INSERT INTO questions (q_id, question, answer, wrong) VALUES (%s, %s, %s, %s)"
    #print("database_insert.DEBUG: my_stmt is: %r" % my_stmt)
    #print("database_insert.DEBUG: my_data is: %r" % my_data)
    #print("database_insert.DEBUG: Trying to cursor.execute() ....")
    cursor.execute(my_stmt, params=None, multi=False)
    #iterator = cursor.execute(my_stmt, params=None, multi=True)
    #cursor.execute(my_stmt, params=None, multi=True)
    #cursor.execute(my_stmt, my_data)
    cursor.close()
    cnx.commit()
    cnx.close()
