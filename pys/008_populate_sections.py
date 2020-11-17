# works as intended
import mysql.connector
from mysql.connector import errorcode
import sys
import re
import os
from os import listdir
from os import system, name 
from os import walk
from os.path import isfile, join
from pprint import pprint as p
import glob

# defines strip_end for variable instantiation
def strip_end(text, suffix):
    if not text.endswith(suffix):
        return text
    return text[:len(text)-len(suffix)]
# assigning some global variables
py_wd=os.getcwd()
#print("DEBUG: thiscwd is: %r" % py_wd)
project_dir=strip_end(py_wd, "/pys")
#print("DEBUG: stripcwd is: %r" % project_dir)
sec_dir=project_dir+"/sections/"
# DEBUG: show properly parsed sections directory
#print("DEBUG: sec_dir is: " + sec_dir)
# Assign sections directory/*txt to this_glob
this_glob=(sec_dir+"*txt")
# DEBUG: show glob
#print("DEBUG: this_glob is: " + this_glob)




### DB METHODS ###
#  
# CALLABLE: db_execute(my_stmt)
# CALLED BY: show_options()
# input: a SELECT statement (my_stmt)
# return: 
def db_select(my_stmt):
  my_rows=''
  line_ct=int(0)
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
    my_rows = cursor.fetchall()
    cursor.close()
    cnx.close()
    for line in my_rows:
      line_ct=line_ct+1
  # return(0,'') by default
  return(line_ct,my_rows)
#  
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
    return 1
  #print("DEBUG: did db_execute(my_stmt) lol")

def find_section_files():
#  f = []
  section_count = 0
  #print(glob.glob("/home/redmage/workspace/linuxtest_delta/sections/*txt"))
  # this should be dynamic, not hardcoded
  #g = glob.glob("/home/redmage/workspace/linuxtest_smoke/sections/*txt")
  g = glob.glob(this_glob)
  # i is a file in the glob of files
  for i in g:
    # section_count should give exact # of section files
    section_count = section_count + 1
    # select an arbitrary file to use
    if section_count == 10:
#      print("DEBUG: arbitrary 10th file: " + i)
      with open(i) as f:
        content = f.readlines()
        for line in content:
          pass
    else:
      pass
  return (section_count, g)
#  print("DEBUG: section count: %s" % section_count)

def list_sections():
  my_stmt = "SELECT * FROM sections;"
  select_results = db_select(my_stmt)
  line_ct=select_results[0]
  rows=select_results[1]
  print("DEBUG: line_ct is: " + str(line_ct))
  for line in rows:
    row0 = str(line[0])
    line1 = str(line[1])
    print("section " + row0 + ":  " + line1)
  #print("DEBUG: listed sections, lol")
  return(line_ct,rows)






def start_populating():
  ## get file info
  count_n_glob=find_section_files() # returns file count [0] and glob [1]
  glob=count_n_glob[1]
  file_count=count_n_glob[0]
  print(file_count) # prints file count
  for a_file in count_n_glob[1]:
    #print(a_file)
    pass
  ## get sections info
  count_n_rows=list_sections() # return db section count [0] and rows [1]
  db_sec_ct=count_n_rows[0]
  #print("DEBUG: db_sec_ct = " + str(db_sec_ct))
  # how do we interact with a non-empty 'section' table?
  drop_or_add=''
  is_success=''
  # drop table if there are more than 0 sections
  if db_sec_ct > 0:
    #print("DEBUG: db_sec_ct is: " + str(db_sec_ct))
    #my_stmt="SHOW TABLES;"
    #my_stmt="INSERT INTO sections (sec_id,sec_name) VALUES (2,'lmao')"
    my_stmt="DROP TABLE sections;"
    is_success=db_interact(my_stmt)
    #print("DEBUG: is_success#0: " + str(is_success))
    print(type(is_success))
   #while drop_or_add == '': 
   #  this_selection=input("DEBUG: drop table or add sections on top? ")
   #  if this_selection == 'drop':
   #    print("DEBUG: ok, DROP is easy")
   #    my_stmt="DROP TABLE sections;"
   #    #is_succcess=db_interact(my_stmt)
   #    this_rand_var=print(db_interact(my_stmt))
   #    print("DEBUG: is_success#0: " + this_rand_var)
   #    # table is dropped and needs to be recreated
    if is_success == int(1) or is_success == 1:
      # creating table sections
      my_stmt = "create table sections (sec_id INT NOT NULL,sec_name VARCHAR(127) NOT NULL);"
      is_success=db_interact(my_stmt)
      #print("DEBUG: is_success#1: " + str(is_success))
      print("DEBUG: dropped sections; created table sections")
   #      if this_rand_var == "1":
   #        print("DEBUG: dropped sections and created sections")
   #        drop_or_add = "complete"
   #        continue
   #    # if we get to return("0") something failed
   #  if this_selection == 'add':
   #    print("DEBUG: that's hard. quitting.")
   #    quit()
   #  if this_selection == 'quit':
   #    print("DEBUG: ok, quitting.")
   #    quit()
  # 
  print("DEBUG: Evaluating files...")
  for i in range(1,file_count+1):
    print('')
    padded_int=(f'{i:02}')
    padded_int=str(padded_int)
    print(padded_int)
    #print(type(padded_int))
    print("DEBUG: searching for padded_int " + padded_int + " in glob..")
    for filename in glob:
      if re.search(padded_int,filename):
        this_file=filename 
        print("DEBUG: [glob].read() [glob]: " + this_file)
        with open(this_file,'r') as file:
          this_section_name=file.read().replace('\n','')
        my_stmt="INSERT INTO sections (sec_id,sec_name) VALUES (" + padded_int + ",'" + this_section_name + "');"
        db_interact(my_stmt)
        #print(my_stmt)
  print('')
  print("Finished processing glob!")

def main():
  start_populating()


main()


############
############
############
############
############




###### UI METHODS ###
####
#### CALLED BY show_options()
#### input: CALLED
#### output: UI clear()
#### imports: system, name
#### credit: https://www.geeksforgeeks.org/clear-screen-python/
###def clear():
###  # for windows 
###  if name == 'nt': 
###    _ = system('cls') 
###  # for mac and linux(here, os.name is 'posix') 
###  else: 
###    _ = system('clear') 
#### CALLABLE: get_confirm_sec_id()
#### CALLED BY 
#### input: null
#### return: INT
#### called by: options()
###def get_confirm_sec_id():
###  shall_i_continue = "no"
###  # input "no" to continue looping
###  while shall_i_continue == "no":
###    this_sec_id = input("Section ID?\n")
###    shall_i_continue = input("Got: section " + this_sec_id + " - no?\n> ")
###  print("DEBUG: get_confirm_sec_id() type(this_sec_id):")
###  print(type(this_sec_id))
###  return(this_sec_id)
###
###def get_confirm_sec_name():
###  shall_i_continue = "no"
###  # input "no" to continue looping
###  while shall_i_continue == "no":
###    this_sec_name = input("This section name?\n> ")
###    shall_i_continue = input("Got: section " + this_sec_name + " - no?\n> ")
###  print("DEBUG: get_confirm_sec_id() type(this_sec_id):")
###  print(type(this_sec_name))
###  return(this_sec_name)
###
###
###
###
####
#### CALLABLE: check_for_section()
#### CALLED BY: various
#### input: user input 
#### return: 0 or [id]
###def check_for_section(this_sec_id):
###  row0='0'
###  #print("DEBUG: got an id: " + this_sec_id)
###  this_stmt = "SELECT * FROM sections WHERE sec_id = " + this_sec_id + ";"
###  #print("DEBUG: this_stmt is: " + this_stmt)
###  count_and_rows = db_execute(this_stmt)
###  result_count = count_and_rows[0]
###  result_count = str(result_count)
###  # if there are no rows, this will bypass
###  print("DEBUG: there are " + result_count + " matches")
###  for row in count_and_rows[1]:
###    print("DEBUG: type(row):")
###    print(type(row))
###    row0 = row[0]
###    row0 = str(row0)
###    print("DEBUG: type(row0):")
###    print(type(row0))
###    print(row0)
###    print("DEBUG: type(this_sec_id):")
###    print(type(this_sec_id))
###    print(this_sec_id)
###    #line1 = str(line[1])
###    #print("I got: section " + row0 + ":  " + line1)
###    if row0 == this_sec_id:
###      print("DEBUG: cool, row0 == this_sec_id, so row0 exists")
###      return(row0)
###  #print("DEBUG: returning row0: " + row0)
###  #print(row0)
###  return(row0)
###  print("DEBUG: checked for section, lol")
####
#### CALLABLE: 
#### CALLED BY show_options()
#### input: user input 
#### return: FAIL or SUCCESS
###def add_section():
###  # get a section ID
###  this_sec_id=get_confirm_sec_id()
###  print("DEBUG: Ok, checking sec_id " + this_sec_id)
###  # checking 
###  rows=check_for_section(this_sec_id)
###  rows0=int(rows[0])
###  if rows0 > 0:
###    print("DEBUG: not adding; rows[0] > 0; section exists")
###    return("0")
###  # confirm this_sec_name as input from get_confirm_sec_name()
###  this_sec_name = get_confirm_sec_name()
###  # this statement accepts this_sec_id and this_sec_name 
###  # and returns hardcoded INSERT statement
###  this_stmt = "INSERT INTO sections (sec_id,sec_name) VALUES (" + this_sec_id + ",'" + this_sec_name + "');"
###  #print("DEBUG: statment is: " + this_stmt)
###  is_success = db_interact(this_stmt) 
###  # db_interact will return "1" if successful
###  if is_success == "1":
###    print("DEBUG: add_section succeeded")
###  #print("DEBUG: Ok, rechecking sec_id for successful add:" + this_sec_id)
###  new_rows=check_for_section(this_sec_id)
###  rows0=str(new_rows[0])
###  if rows0 == this_sec_id:
###    print("DEBUG: confirmed add_section succeeded")
###    return(rows0)
###  else:
###    quit()
###  #print("DEBUG: this_stmt: " + this_stmt)
###  print("DEBUG: tried to add section, lol")
####
#### CALLABLE:
#### CALLED BY: show_options()
#### input:
#### return:
###def del_section():
###  # get a section ID
###  this_sec_id=get_confirm_sec_id()
###  print("DEBUG: Ok, checking sec_id " + this_sec_id)
###  # checking 
###  rows=check_for_section(this_sec_id)
###  rows0=str(rows[0])
###  #print("DEBUG: rows0: " + rows0)
###  #print("DEBUG: this_sec_id: " + this_sec_id)
###  print(type(rows0))
###  print(type(this_sec_id))
###  if rows0 == this_sec_id:
###    print("DEBUG: section exists; can be deleted")
###  if rows0 != this_sec_id:
###    print("DEBUG: section does not exist; returning")
###    return("0")
###  # this statement accepts this_sec_id and this_sec_name 
###  # and returns hardcoded INSERT statement
###  this_stmt = "DELETE FROM sections WHERE sec_id = '" + this_sec_id + "';"
###  print("DEBUG del_section(): statment is: " + this_stmt)
###  is_success = db_interact(this_stmt) 
###  # db_interact will return "1" if successful
###  if is_success == "1":
###    print("DEBUG: del_section succeeded")
###  else:
###    return("0")
###  #print("DEBUG: Ok, rechecking sec_id for successful add:" + this_sec_id)
###  new_rows=check_for_section(this_sec_id)
###  rows0=str(new_rows[0])
###  # rows0 should be 0 if row is deleted
###  if rows0 != this_sec_id:
###    print("DEBUG: confirmed delete succeeded")
###    return("1")
###  else:
###    return("0")
###    quit()
###  #print("DEBUG: this_stmt: " + this_stmt)
###  print("DEBUG: tried to add section, lol")
###
#### CALLABLE: show_options
#### CALLED BY: main()
#### input: user input
#### return: list of options
#### output: function()
###def show_options():
###  my_response = ''
###  this_sec_id = "1"
###  while my_response == '':
###    clear()
###    print("show_options:")
###    print("0. list_sections")
###    print("1. check_for_section(get_confirm_sec_id())")
###    print("2. add_section")
###    print("3. del_section")
###    print("Q. quit")
###    print("")
###    my_response=input("Input: select option\n")
###    print("")
###    if my_response == "0":
###      list_sections() #
###    if my_response == "1":
###      check_for_section(get_confirm_sec_id()) #
###    if my_response == "2":
###      add_section()
###    if my_response == "3":
###      del_section()
###    if my_response == "q" or my_response == "Q":
###      sys.exit()
###    sleep(4)
###    my_response = ''
###
###def main():
###  show_options()
###
###
###############
###############
###main()
