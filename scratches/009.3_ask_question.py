# beta version; see 009.5
import os
import subprocess
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
  #print("DEBUG: got: %r" % q_id) # print q_id from database
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
  # a_5 is generally going to be NULL from the database
  # we're not handling for that now but this logic should work
  if a_5 == "None" or "" or "None,":
    #print("DEBUG: rand_int is: ")
    #print(rand_int)
    a_5=("Some of the above, maybe!")
#    if rand_int == 0 or rand_int == 1 or rand_int == 2 \
#        or rand_int == 3 or rand_int == 4 or rand_int == 5 \
#        or rand_int == 6 or rand_int == 7:
#      op_1=('A',str(a_4))
#      op_2=('B',str(a_2))
#      op_3=('C',str(a_3))
#      op_4=('D',str(a_1))
#      op_5=('E',str(a_5))
    if rand_int == 0: 
      op_1=('A',str(a_4))
      op_2=('B',str(a_2))
      op_3=('C',str(a_3))
      op_4=('D',str(a_1))
      op_5=('E',str(a_5))
    if rand_int == 1: 
      op_1=('A',str(a_3))
      op_2=('B',str(a_2))
      op_3=('C',str(a_1))
      op_4=('D',str(a_4))
      op_5=('E',str(a_5))
    if rand_int == 2: 
      op_1=('A',str(a_2))
      op_2=('B',str(a_3))
      op_3=('C',str(a_1))
      op_4=('D',str(a_4))
      op_5=('E',str(a_5))
    if rand_int == 3: 
      op_1=('A',str(a_2))
      op_2=('B',str(a_4))
      op_3=('C',str(a_1))
      op_4=('D',str(a_3))
      op_5=('E',str(a_5))
    if rand_int == 4: 
      op_1=('A',str(a_1))
      op_2=('B',str(a_4))
      op_3=('C',str(a_3))
      op_4=('D',str(a_2))
      op_5=('E',str(a_5))
    if rand_int == 5: 
      op_1=('A',str(a_1))
      op_2=('B',str(a_2))
      op_3=('C',str(a_4))
      op_4=('D',str(a_3))
      op_5=('E',str(a_5))
    if rand_int == 6: 
      op_1=('A',str(a_1))
      op_2=('B',str(a_3))
      op_3=('C',str(a_4))
      op_4=('D',str(a_2))
      op_5=('E',str(a_5))
    if rand_int == 7: 
      op_1=('A',str(a_1))
      op_2=('B',str(a_2))
      op_3=('C',str(a_3))
      op_4=('D',str(a_4))
      op_5=('E',str(a_5))
  return(op_1,op_2,op_3,op_4,op_5)

def eval_answer(letter,option,correct_a):
  print("DEBUG: letter is:" + letter)
  print("DEBUG option is: " + option)
  # correct_a is a list object at this point; cast as str
  correct_a=str(correct_a)
  correct_a=correct_a.rpartition("[('")[2]
  correct_a=correct_a.rstrip("',)]")
  print("DEBUG: correct_a is: " + correct_a)
  if option == correct_a:
      return("Probably correct! Nice")
  else:
      return("Probably not correct!")
  #return("Correct, probably!")

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
    question,correct_a,incorrect_1,incorrect_2,incorrect_3,incorrect_4 = test_question(q_id)
    #print("DEBUG: incorrect_4 is: %r") % incorrect_4
    (op_1,op_2,op_3,op_4,op_5)=randomizer(correct_a,incorrect_1,incorrect_2,incorrect_3,incorrect_4,this_rand)
    question=str(question)
    question=question.rpartition("[('")[2]
    question=question.rstrip("',)]")
    print(question)
    print("possible answers:")
    #print(type(op_1))
    #print(op_1[0])
    #print(op_1[1])
    # strings come to us formatted this way: "[('$ ps',)]"
    op_1_str=op_1[1].rpartition("[('")[2]
    op_1_str=op_1_str.rstrip("',)]")
    op_2_str=op_2[1].rpartition("[('")[2]
    op_2_str=op_2_str.rstrip("',)]")
    op_3_str=op_3[1].rpartition("[('")[2]
    op_3_str=op_3_str.rstrip("',)]")
    op_4_str=op_4[1].rpartition("[('")[2]
    op_4_str=op_4_str.rstrip("',)]")
    op_5_str=op_5[1].rpartition("[('")[2]
    op_5_str=op_5_str.rstrip("',)]")
    #print(op_1[1])
    #op_1=op_1.rpartition(",)]")[2]
    #op_1 = re.sub(r'\\n','',op_1)
    #op_1=re.sub(',)]','',op_1)
    print("A. " + op_1_str)
    print("B. " + op_2_str)
    print("C. " + op_3_str)
    print("D. " + op_4_str)
    print("E. " + op_5_str)
    print("")
    # reinstantiate my_answer per loop
    my_ops = [op_1, op_2, op_3, op_4, op_5]
    my_answer=''
    my_answer=input("Your answer? ")
    print("I answered: %s" % my_answer)
    print("")
    if my_answer == 'A' or my_answer == 'a':
      print("DEBUG: got A")
      for i in my_ops:
        #print(i[0])
        if i[0] == "A" or i[0] == "a":
          this_op_str=i[1].rpartition("[('")[2]
          this_op_str=this_op_str.rstrip("',)]")
          eval_return=eval_answer(my_answer,this_op_str,correct_a)
          print("it's this one")
    elif my_answer == 'B' or my_answer == 'b':
      #print("DEBUG: got B")
      for i in my_ops:
        #print(i[0])
        if i[0] == "B" or i[0] == "b":
          this_op_str=i[1].rpartition("[('")[2]
          this_op_str=this_op_str.rstrip("',)]")
          eval_return=eval_answer(my_answer,this_op_str,correct_a)
          print("it's this one")
      pass
    elif my_answer == 'C' or my_answer == 'c':
      #print("DEBUG: got C")
      for i in my_ops:
        #print(i[0])
        if i[0] == "C" or i[0] == "c":
          this_op_str=i[1].rpartition("[('")[2]
          this_op_str=this_op_str.rstrip("',)]")
          eval_return=eval_answer(my_answer,this_op_str,correct_a)
          print("it's this one")
      pass
    elif my_answer == 'D' or my_answer == 'd':
      #print("DEBUG: got D")
      for i in my_ops:
        #print(i[0])
        if i[0] == "D" or i[0] == "d":
          this_op_str=i[1].rpartition("[('")[2]
          this_op_str=this_op_str.rstrip("',)]")
          eval_return=eval_answer(my_answer,this_op_str,correct_a)
          print("it's this one")
      pass
    elif my_answer == 'E' or my_answer == 'e':
      #print("DEBUG: got E")
      for i in my_ops:
        #print(i[0])
        if i[0] == "E" or i[0] == "e":
          this_op_str=i[1].rpartition("[('")[2]
          this_op_str=this_op_str.rstrip("',)]")
          eval_return=eval_answer(my_answer,this_op_str,correct_a)
          print("it's this one")
      pass
    elif my_answer == 'quit':
      print("DEBUG: got quit")
      exit()
    else:
      print("DEBUG: derp; halt")
      exit()
    #print("DEBUG:%r"%type(my_answer))
    #print("DEBUG:%r"%type(op_1))
    #print("DEBUG:%r"%type(correct_a))
    # test the eval_return() method
    #eval_return=eval_answer(my_answer,op_1_str,correct_a)
    print("")
    print("DEBUG: " + eval_return)
    print("")
#    question_stuff = test_question(q_id)
#    for i in question_stuff:
#      print(i)
  return 0

main()


