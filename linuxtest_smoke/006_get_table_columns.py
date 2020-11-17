# works as intended
import mysql.connector
from mysql.connector import errorcode
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

line_count = 0
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

def get_table_columns():
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
    cursor.execute("DESCRIBE questions;")
    my_columns = cursor.fetchall()
    cursor.close()
  for (a_column) in my_columns:
#    line_count = line_count + 1
    print(a_column)
#  print("DEBUG: line_count is: %s" % line_count)
  return my_columns

get_table_columns()

#print(my_columns)
