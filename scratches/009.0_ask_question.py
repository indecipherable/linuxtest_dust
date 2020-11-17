import os
from os import listdir
from os.path import isfile, join
from os import walk
import mysql.connector
from mysql.connector import errorcode
import glob
import re

# VARIABLES ASSIGNMENT BEGIN
# defines strip_end for project_dir instantiation
def strip_end(text, suffix):
    if not text.endswith(suffix):
        return text
    return text[:len(text)-len(suffix)]
# enumerate where our project files are
py_wd=os.getcwd()
#print("DEBUG: thiscwd is: %r" % py_wd)
project_dir=strip_end(py_wd, "/pys")
#print("DEBUG: stripcwd is: %r" % project_dir)
table_dir=project_dir+"/database_tables/"
# Assign databases directory/*txt to this_glob
this_glob=(table_dir+"create*que*txt")

def get_question_ids(sec_id):
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
    cursor = cnx.cursor(buffered=True)
    #this_statement="SELECT q_id FROM questions WHERE sec_id=%r;" % sec_id
    #print("DEBUG: %r" % this_statment
    select_stmt = "SELECT q_id FROM questions WHERE sec_id=%(sec_id)s"
    cursor.execute(select_stmt, { 'sec_id': sec_id })
    q_ids = cursor.fetchall()
    #cursor.execute(this_statement, params=None, multi=False) % sec_id
    #cursor.execute("%r") % this_statement
    #q_ids = cursor.fetchall(this_statement, params=None, multi=False) % sec_id
    #print("DEBUG: q_ids is: %r" % q_ids)
    #cnx.commit()
    cursor.close()
  #cnx.close()
  return (q_ids)

def get_column_values(a_table):
  ########
  ## begin SQL querying
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
    #print("DEBUG: no exception, get my_columns")
    cursor = cnx.cursor()
    cursor.execute("DESCRIBE questions;")
    my_columns = cursor.fetchall()
    cursor.close()
  ### end SQL querying
  ########
  ### begin assignment
  column_count = 0
  # for each column fetched to my_columns by cursor.fetchall()
  for a_column in my_columns:
    # debug to show column_count
    #print("get_column_values.DEBUG: column_count is: %r" % column_count)
    # increment
    column_count += 1
  #return column_count
  # reset column_count for inserts
  # instantiate column_name_list with arbitrary number of columns
  #print("DEBUG: Column_count is: %r" % column_count)
  column_title_list = [[]] * column_count
  column_datatype_list = [[]] * column_count
  column_null_ok_list = [[]] * column_count
  column_is_key_list = [[]] * column_count
  column_count = 0
  #print("DEBUG: column_name_list is: %r" % column_name_list)
  for a_column in my_columns:
    #print("DEBUG: Column_list is: %r" % column_name_list)
    #print("DEBUG: Column_count is: %r" % column_count)
    #print("DEBUG: a_column[0] is: %r" % a_column[0])
    # assign get_columns[index] to column_name_list[index]
    column_title_list[column_count] = a_column[0]
    #print("DEBUG: a_column[1] is: %r" % a_column[1]) # datatype
    column_datatype_list[column_count] = a_column[1]
    #print("DEBUG: a_column[2] is: %r" % a_column[2]) # is_required
    column_null_ok_list[column_count] = a_column[2]
    #print("DEBUG: a_column[3] is: %r" % a_column[3])
    column_is_key_list[column_count] = a_column[3]
    # increment column_count
    column_count += 1
  #print("get_column_values.debug shows column_count: %r" % column_count) # 9 
  return (column_count, column_title_list, column_datatype_list, column_null_ok_list, column_is_key_list)

def test_question(q_id):
  try:
    # create mysql connector object
    cnx = mysql.connector.connect(user='root', password='nice_password',
                                  host='127.0.0.1', database='linuxquiztest')
    cursor = cnx.cursor(buffered=True)
  # handle ER_ACCESS_DENIED_ERROR, ER_BAD_DB_ERROR
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
    raise
  else:
    cursor = cnx.cursor(buffered=True)
    select_stmt = "SELECT question FROM questions WHERE q_id=%(q_id)s"
    cursor.execute(select_stmt, { 'q_id': q_id })
    this_question = cursor.fetchall()
    for (q_id, sec_id, question, correct_a) in cursor:
      print("DEBUG: {}, {}, {}, {}".format(q_id,sec_id,question,correct_a))
    cursor.close()
    cnx.commit()
    cnx.close()
#    print("create_tables succeeded probably!")
  return (this_question)

def main():
  section_I_want=input("Which section do you want to do? ")
  print("You want to look at section %r, cool" % section_I_want)
  question_ids=get_question_ids(section_I_want)
  #column_count, column_title_list, column_datatype_list, column_null_ok_list, column_is_key_list=get_column_values("questions")
  #print(column_count)
  #var0=column_title_list[0] # column
  #var1=column_title_list[1] # column
  #var2=column_title_list[2] # question column
  #var3=column_title_list[3] # correct_a column
  #var4=column_title_list[4] # incorrect_1 column
  #var5=column_title_list[5] # incorrect_2 column
  #var6=column_title_list[6] # incorrect_3 column
  #var7=column_title_list[7] # incorrect_4 column
  #print(var0)
  for q_id in question_ids:
    #print()
    #print("DEBUG: %r" % q_id)
    this_question = test_question(q_id)
    for a_field in this_question:
      print(a_field)
    #statement='SELECT q_id, sec_id, question, correct_a FROM questions HAVING q_id=%r;' % q_id
    #statement='SELECT %r, %r, %r, %r FROM questions HAVING q_id=%r;' % (var0, var1, var2, var3, q_id)
    #get_question(statement)
    #print("DEBUG: " + statement)
  return 0

main()
