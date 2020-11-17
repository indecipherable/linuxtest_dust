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
# this is not a dynamic reference - TO-DO
project_dir=strip_end(py_wd, "/linuxtest_smoke")
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
  for i in glob:
    print("DEBUG: got i for glob:")
    print(i)
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
    print("Found more than 0 db sections in table")
    print("Add sections not working; you will lose data")
    seriously=input("Drop table anyway?")
    if seriously == "yes" or seriously == "y" or seriously == "Y" or seriously == "YES":
      pass
    else:
      exit
    #print("DEBUG: db_sec_ct is: " + str(db_sec_ct))
    #my_stmt="SHOW TABLES;"
    #my_stmt="INSERT INTO sections (sec_id,sec_name) VALUES (2,'lmao')"
    my_stmt="DROP TABLE sections;"
    is_success=db_interact(my_stmt)
    #print("DEBUG: is_success#0: " + str(is_success))
    print("DEBUG: type(is_success):")
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
  print("file_count is: " + str(file_count))
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

