# this is a scratch file
# use with caution
import glob
import sys
import re
import os
from os import listdir
from os.path import isfile, join
from os import walk
from pprint import pprint as p
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
num_table_fields = 0

def sql_insertor():
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

#sql_insertor(realpath_file)
def sql_insertor_test(realpath_file, id):
  # this is OK
  print("DEBUG: showing realpath and id: %s %s" % (realpath_file, id))
  print("DEBUG: field count of questions is: %s" % num_table_fields )
  #num_file_lines = sum(1 for line in open(realpath_file))
  print("DEBUG: line count of realpath_file is: %s" % num_file_lines) 

def main():
  question_count = 0
  g = glob.glob("/home/redmage/workspace/linuxtest_delta/questions/*txt")
  for i in g:
      question_count = question_count + 1
      print i
      sql_insertor_test(i, question_count)
  #print("DEBUG: question count: %s" % question_count)
  #mypath="/home/redmage/workspace/linuxtest_delta/questions/"

main()

