# works as intended
# developmental
# see ../scratches/009.[-n]*
import db_interact
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

# randomizer returns a randomized list of options as Key-Value tuplets: (CHAR,STRING)
def randomizer(a_1,a_2,a_3,a_4,a_5,rand_int):
  # we're mostly handling for 4 options right now:
  # one correct one, and three incorrect ones
  op_5 = "none of the above, probably"
  # a_5 is generally going to be NULL from the database
  # we're not handling for that now but this logic should work
  if a_5 == "None" or "" or "None,":
    #print("DEBUG: rand_int is: ")
    #print(rand_int)
    a_5=("Zero of the above, I guess?!")
    # dummy randomize for testing
#    if rand_int == 0 or rand_int == 1 or rand_int == 2 \
#        or rand_int == 3 or rand_int == 4 or rand_int == 5 \
#        or rand_int == 6 or rand_int == 7:
    # base option tuple instantiation
    op_1=('A',str(a_1))
    op_2=('B',str(a_2))
    op_3=('C',str(a_3))
    op_4=('D',str(a_4))
    op_5=('E',str(a_5))
    # permute options by rand_int value
    if rand_int == 0: 
      op_1=('A',str(a_4))
      op_4=('D',str(a_1))
    elif rand_int == 1: 
      op_1=('A',str(a_3))
      op_2=('B',str(a_2))
      op_3=('C',str(a_1))
    elif rand_int == 2: 
      op_1=('A',str(a_2))
      op_2=('B',str(a_3))
      op_3=('C',str(a_1))
      op_4=('D',str(a_4))
    elif rand_int == 3: 
      op_1=('A',str(a_2))
      op_2=('B',str(a_4))
      op_3=('C',str(a_1))
      op_4=('D',str(a_3))
    elif rand_int == 4: 
      op_2=('B',str(a_4))
      op_4=('D',str(a_2))
    elif rand_int == 5: 
      op_2=('B',str(a_2))
      op_3=('C',str(a_4))
      op_4=('D',str(a_3))
    elif rand_int == 6: 
      op_2=('B',str(a_3))
      op_3=('C',str(a_4))
      op_4=('D',str(a_2))
    elif rand_int == 7: 
      op_2=('B',str(a_4))
      op_3=('C',str(a_3))
      op_4=('D',str(a_2))
    else:
      print("DEBUG: got a bad option; exiting.")
      exit()
  # return randomized options
  return(op_1,op_2,op_3,op_4,op_5)

# check_response inputs: 
# (this_answer:CHAR, my_ops:LIST, correct_a:STR)
# check_response function:
# validate an answer 
#
# this sanitizes input for eval_answer
def check_response(this_answer,my_ops,correct_a):
    # evaluate this_answer for [A-E],[a-e] validity against my_ops[0]
    if this_answer == 'A' or this_answer == 'a':
      #print("DEBUG: got A")
      # i is a tuple of options: (CHAR,STRING)
      # my_ops is a list of tuplets of randomized key-value letter-answer
      # possible TO-DO - collapse this?
      for i in my_ops:
        #print(i[0])
        if i[0] == "A" or i[0] == "a":
          i_tup_str=i[1].rpartition("[('")[2]
          i_tup_str=i_tup_str.rstrip("',)]")
          # my_answer is return() from eval_answer()
          # return: int,letter
          my_answer=eval_answer(this_answer,i_tup_str,correct_a)
          return(my_answer)
    elif this_answer == 'B' or this_answer == 'b':
      #print("DEBUG: got B")
      for i in my_ops:
        #print(i[0])
        if i[0] == "B" or i[0] == "b":
          i_tup_str=i[1].rpartition("[('")[2]
          i_tup_str=i_tup_str.rstrip("',)]")
          # my_answer is return() from eval_answer()
          # return: int,letter
          my_answer=eval_answer(this_answer,i_tup_str,correct_a)
          return(my_answer)
      pass
    elif this_answer == 'C' or this_answer == 'c':
      #print("DEBUG: got C")
      for i in my_ops:
        #print(i[0])
        if i[0] == "C" or i[0] == "c":
          i_tup_str=i[1].rpartition("[('")[2]
          i_tup_str=i_tup_str.rstrip("',)]")
          # my_answer is return() from eval_answer()
          # return: int,letter
          my_answer=eval_answer(this_answer,i_tup_str,correct_a)
          return(my_answer)
      pass
    elif this_answer == 'D' or this_answer == 'd':
      #print("DEBUG: got D")
      for i in my_ops:
        #print(i[0])
        if i[0] == "D" or i[0] == "d":
          i_tup_str=i[1].rpartition("[('")[2]
          i_tup_str=i_tup_str.rstrip("',)]")
          # my_answer is return() from eval_answer()
          # return: int,letter
          my_answer=eval_answer(this_answer,i_tup_str,correct_a)
          return(my_answer)
      pass
    elif this_answer == 'E' or this_answer == 'e':
      #print("DEBUG: got E")
      for i in my_ops:
        #print(i[0])
        if i[0] == "E" or i[0] == "e":
          i_tup_str=i[1].rpartition("[('")[2]
          i_tup_str=i_tup_str.rstrip("',)]")
          # my_answer is return() from eval_answer()
          # return: int,letter
          my_answer=eval_answer(this_answer,i_tup_str,correct_a)
          return(my_answer)
      pass
    # we should be getting sanitized inputs to check_response() from run_test() 
    #   but hey, stranger things have happened
    elif this_answer == "U" or this_answer == "u" or this_answer == "unsure": 
      my_answer=eval_answer(this_answer,"unsure",correct_a)
      return(my_answer)
    else:
      print("DEBUG: unhandled response, oops.")
      exit()

# input: letter INT,answer STR, correct_a STR
def eval_answer(letter,answer,correct_a):
  #print("DEBUG: letter is: " + letter)
  #print("DEBUG: answer is: " + answer)
  # correct_a is a list object at this point; cast as str
  correct_a=str(correct_a)
  correct_a=correct_a.rpartition("[('")[2]
  correct_a=correct_a.rstrip("',)]")
  print("DEBUG: correct_a is: " + correct_a)
  if answer == correct_a:
      print("DEBUG: answer is: " + answer)
      #return("Probably correct! Nice")
      return(int(1),letter)
  elif answer == "unsure":
      print("DEBUG: answer is: " + answer)
      #return("Probably correct! Nice")
      return(int(0),letter)
  else:
      print("DEBUG: answer is: " + answer)
      #return("Probably not correct!")
      return(int(-1),letter)
  #return("Correct, probably!")

def process_session(section_I_want,section_score,section_answer_tuple_list):
  print("DEBUG: running process_section()")
  print("DEBUG: input (section_I_want,section_score,section_answer_tuple_list)")
  print("DEBUG: section_I_want: " + section_I_want)
  print("DEBUG: section_score: " + section_score)
  print("DEBUG: section_answer_tuple_list: " + section_answer_tuple_list)

def check_stats():
  print("DEBUG: running check_stats()")

def run_test():
  # section_I_want is a TO-DO
  #section_I_want=2
  section_I_want=input("Which section do you want to do? ")
  print("You want to look at section %r, cool" % section_I_want)
  question_ids=get_question_ids(section_I_want)
  section_score=0
  section_q_count=0
  section_answer_tuple_list=[[]]
  for q in question_ids:
    section_q_count=section_q_count+1
    #print("DEBUG: %r questions found" % section_q_count)
    #print("DEBUG: we got %r section_q_count" % section_q_count)
  for q_id in question_ids:
    print("")
    print("")
    #print(q_id)
    this_rand=get_random()
    #print("this_rand = %r") % this_rand
    #print(this_rand)
    question,correct_a,incorrect_1,incorrect_2,incorrect_3,incorrect_4 = test_question(q_id)
    #print("DEBUG: incorrect_4 is: %r") % incorrect_4
    # randomizer returns a randomized list of options as Key-Value tuplets: (CHAR,STRING)
    (op_1,op_2,op_3,op_4,op_5)=randomizer(correct_a,incorrect_1,incorrect_2,incorrect_3,incorrect_4,this_rand)
    question=str(question)
    question=question.rpartition("[('")[2]
    question=question.rstrip("',)]")
    print(question)
    print("possible answers:")
    #print(type(op_1))
    #print(op_1[0])
    #print(op_1[1])
    # strings come to us formatted this way: "[('$ ps',)]" from randomizer(..)
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
    # Presents a list of optional answers:
    print("A. " + op_1_str)
    print("B. " + op_2_str)
    print("C. " + op_3_str)
    print("D. " + op_4_str)
    print("E. " + op_5_str)
    print("")
    # reinstantiate my_answer per loop
    my_answer=''
    # instantiate my_ops
    my_ops = [op_1, op_2, op_3, op_4, op_5]
    this_answer=input("Your answer? ")
    #print("DEBUG: I answered: %s" % this_answer)
    print("")
    # loop until we have a valid input, quit, or retry
    while my_answer == '':
      # if we get an answer that's an appropriate answer, char A-E,a-e
      if this_answer == 'A' or this_answer == 'a' or \
         this_answer == 'B' or this_answer == 'b' or \
         this_answer == 'C' or this_answer == 'c' or \
         this_answer == 'D' or this_answer == 'd' or \
         this_answer == 'E' or this_answer == 'e':
         # then check the answer against tuples of randomized options
         # and return a value which will PASS the loop
         my_answer=check_response(this_answer,my_ops,correct_a)
         #print("DEBUG: my_answer[0] is: " + my_answer[0])
         #print("DEBUG: my_answer[0] is: " + my_answer[1])
         #this_type=type(my_answer)
         #print("DEBUG: type(my_answer) is: %r" % this_type)
         #section_answer_tuple_list=section_answer_tuple_list.append(my_answer)
         pass
      elif this_answer == 'U' or this_answer == 'u' or this_answer == "unsure":
         my_answer=check_response(this_answer,my_ops,correct_a)
         pass
      elif this_answer == 'quit' or this_answer == 'QUIT' or this_answer == "Quit":
        print("DEBUG: Quitting without saving session info.")
        exit()
      else:
        print("DEBUG: unhandled response: " + this_answer)
        this_answer=""
        this_answer=input("Try again: ")
        print("")
    # check_response returns: 
    print("RUN: OK, my_answer[0] is: " + str(my_answer[0]))
    if my_answer[0] == -1:
      print("DEBUG: got -1, adding -1")
      section_score=section_score-1
    elif my_answer[0] == 0:
      print("DEBUG: got 1, adding 0")
      section_score=section_score+0
    elif my_answer[0] == 1:
      print("DEBUG: got 1, adding 1")
      section_score=section_score+1
    else:
      print("DEBUG: question should be correct or incorrect.")
      exit()
    print("RUN: OK, my_answer[1] is: " + str(my_answer[1]))
    # test the eval_return() method
    #eval_return=eval_answer(my_answer,op_1_str,correct_a)
    print("")
    print("")
#    question_stuff = test_question(q_id)
#    for i in question_stuff:
#      print(i)
  print("RUN: section_score is: %r out of %r" % ( section_score, section_q_count ) ) 
  #print("DEBUG: section_answer_tuple_list:" + section_answer_tuple_list)
#  for an_answer_tuple in section_answer_tuple_list:
#    print("DEBUG: " + an_answer_tuple[1])
#    print("DEBUG: " + an_answer_tuple[2])
  #process_session(section_I_want,section_score,section_answer_tuple_list)
  return 0


def main():
  print("### WELCOME TO LINUXQUIZTEST ###")
  print("")
  print("  - menu options -")
  print("run_test")
  print("check_stats")
  print("")
  menu_option=input("Do what now? > ")
  if menu_option == "run_test":
    run_test()
    return 0
  if check_stats == "check_stats":
    check_stats()
    return 0
  exit()

if __name__ == "__main__":
  main()

