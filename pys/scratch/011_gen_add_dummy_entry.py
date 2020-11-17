import sys
import re
import os
from pprint import pprint as p
# trying to import where_am_i as module
#import importlib
#where_am_i="/000_where_am_i"
#sys.path.append(os.getcwd())
#import 000_where_am_i
#pm = __import__(where_am_i)
#find_where_am_i()
import mysql.connector
from mysql.connector import errorcode



# defines strip_end for project_dir
def strip_end(text, suffix):
    if not text.endswith(suffix):
        return text
    return text[:len(text)-len(suffix)]
# enumerate where our project directories are
#print("DEBUG: sys.path is: %r" % sys.path)
py_wd=os.getcwd()
#print("DEBUG: thiscwd is: %r" % py_wd)
project_dir=strip_end(py_wd, "/pys")
#print("DEBUG: stripcwd is: %r" % project_dir)
q_dir=project_dir+"/questions"
#print("DEBUG: q_dir is: %r" % q_dir)

def sql_insertor():
  try:
    cnx = mysql.connector.connect(user='graymage', password='my_password',
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
#    entry_generator("0101.txt")
    my_data = ["3", 'Is the sky green', 'no', 'yes']
    my_stmt = "INSERT INTO dummy_questions (q_id, question, answer, wrong) VALUES (%s, %s, %s, %s)"
    #print("my_stmt is: \n%r" % my_stmt)
    #my_data = "('', 'Is the sky blue?', 'yes', 'no')"
    #my_data = "("", "Is the sky blue?", "yes", "no")"
    #print("DEBUG: 'my_data is: \n%r" % my_data)
    # commit entry to database via connector
    cursor.execute(my_stmt, my_data)
    #cursor.executemany(my_stmt, my_data)
    # entry_generator(my_file)
    cnx.commit()
    print("records inserted")
    cursor.close()
    cnx.close()

sql_insertor()
