# beta version; see 009.5
import subprocess
import os
#import random
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

def get_random():
  cmd = 'python3 rand.py'
  p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
  out, err = p.communicate()
  # cast bytes object as string
  result = str(out)
  #print(type(result))
  #result = re.sub(r"b''","",result)
  #result = re.sub(r"\\n\'","",result)
  # result at this point is b'[int]\b'
  result = result.rpartition("b'")[2]
  result = re.sub(r'\\n\'','',result)
  # cast string as int
  result = int(result)
  #print(type(result))
  # this should result an int
  #print(result)
  return(result)

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
    select_stmt = "SELECT q_id FROM questions WHERE sec_id=%(sec_id)s"
    cursor.execute(select_stmt, { 'sec_id': sec_id })
    q_ids = cursor.fetchall()
    cursor.close()
  cnx.close()
  return (q_ids)

def test_question(q_id):
  print("DEBUG: got: %r" % q_id)
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
    select_stmt = "SELECT question FROM questions WHERE q_id=%s" % q_id
    cursor.execute(select_stmt)
    question = cursor.fetchall()
    select_stmt = "SELECT correct_a FROM questions WHERE q_id=%s" % q_id
    cursor.execute(select_stmt)
    correct_a = cursor.fetchall()
    select_stmt = "SELECT incorrect_1 FROM questions WHERE q_id=%s" % q_id
    cursor.execute(select_stmt)
    incorrect_1  = cursor.fetchall()
    select_stmt = "SELECT incorrect_2 FROM questions WHERE q_id=%s" % q_id
    cursor.execute(select_stmt)
    incorrect_2 = cursor.fetchall()
    select_stmt = "SELECT incorrect_3 FROM questions WHERE q_id=%s" % q_id
    cursor.execute(select_stmt)
    incorrect_3 = cursor.fetchall()
    select_stmt = "SELECT incorrect_4 FROM questions WHERE q_id=%s" % q_id
    cursor.execute(select_stmt)
    incorrect_4 = cursor.fetchall()
    cursor.close()
  cnx.close()
  return (question,correct_a,incorrect_1,incorrect_2,incorrect_3,incorrect_4)

def randomizer(a_1,a_2,a_3,a_4,a_5,rand_int):
  #randnum=randrange(0,7)
  op_5 = "none of the above, probably"
  #rand_int = int(rand_int)
  #print("DEBUG: rand_int is: %r") % rand_int
  #print("DEBUG: type(rand_int) is: %r") % type(rand_int)
  #print("DEBUG: rand_int is:")
  #print(rand_int)
  if a_5 == "None" or "" or "None,":
    print("rand_int is: ")
    print(rand_int)
    a_5=("Some of the above, maybe!")
    if rand_int == 0: 
      op_1=a_4
      op_2=a_2
      op_3=a_3
      op_4=a_1
      op_5=a_5
    if rand_int == 1: 
      op_1=a_3
      op_2=a_2
      op_3=a_1
      op_4=a_4
      op_5=a_5
    if rand_int == 2: 
      op_1=a_2
      op_2=a_3
      op_3=a_1
      op_4=a_4
      op_5=a_5
    if rand_int == 3: 
      op_1=a_2
      op_2=a_4
      op_3=a_1
      op_4=a_3
      op_5=a_5
    if rand_int == 4: 
      op_1=a_1
      op_2=a_4
      op_3=a_3
      op_4=a_2
      op_5=a_5
    if rand_int == 5: 
      op_1=a_1
      op_2=a_2
      op_3=a_4
      op_4=a_3
      op_5=a_5
    if rand_int == 6: 
      op_1=a_1
      op_2=a_3
      op_3=a_4
      op_4=a_2
      op_5=a_5
    if rand_int == 7: 
      op_1=a_1
      op_2=a_2
      op_3=a_3
      op_4=a_4
      op_5=a_5
  return(op_1,op_2,op_3,op_4,op_5)

def main():
  section_I_want=input("Which section do you want to do? ")
  #section_I_want=2
  print("You want to look at section %r, cool" % section_I_want)
  question_ids=get_question_ids(section_I_want)
  for q_id in question_ids:
    print("")
    print("")
    #print(q_id)
    this_rand=get_random()
    #print("this_rand = %r") % this_rand
    #print(this_rand)
    question,correct_a,incorrect_1,incorrect_2,incorrect_3,incorrect_4 = test_question(q_id)
    #print("DEBUG: incorrect_4 is: %r") % incorrect_4
    (op_1,op_2,op_3,op_4,op_5)= randomizer(correct_a,incorrect_1,incorrect_2,incorrect_3,incorrect_4,this_rand)
    print(question)
    print("possible answers:")
    print(type(op_1))
    #print("A. %s") % op_1
    #print("B. %s") % op_2
    #print("C. %s") % op_3
    #print("D. %s") % op_4
    #print("E. %s") % op_5
    print("")
    my_answer=input("Your answer? ")
    print("I answered: %s") % my_answer
#    question_stuff = test_question(q_id)
#    for i in question_stuff:
#      print(i)
  return 0

main()


