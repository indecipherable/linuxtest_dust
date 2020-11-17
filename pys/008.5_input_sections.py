# works as intended
import mysql.connector
from mysql.connector import errorcode
import sys
import re
import os
from os import system, name 
from pprint import pprint as p
from time import sleep

### UI METHODS ###
#
# CALLED BY show_options()
# input: CALLED
# output: UI clear()
# imports: system, name
# credit: https://www.geeksforgeeks.org/clear-screen-python/
def clear():
  # for windows 
  if name == 'nt': 
    _ = system('cls') 
  # for mac and linux(here, os.name is 'posix') 
  else: 
    _ = system('clear') 
# CALLABLE: get_confirm_sec_id()
# CALLED BY 
# input: null
# return: INT
# called by: options()
def get_confirm_sec_id():
  shall_i_continue = "no"
  # input "no" to continue looping
  while shall_i_continue == "no":
    this_sec_id = input("Section ID?\n")
    shall_i_continue = input("Got: section " + this_sec_id + " - no?\n> ")
  print("DEBUG: get_confirm_sec_id() type(this_sec_id):")
  print(type(this_sec_id))
  return(this_sec_id)

def get_confirm_sec_name():
  shall_i_continue = "no"
  # input "no" to continue looping
  while shall_i_continue == "no":
    this_sec_name = input("This section name?\n> ")
    shall_i_continue = input("Got: section " + this_sec_name + " - no?\n> ")
  print("DEBUG: get_confirm_sec_id() type(this_sec_id):")
  print(type(this_sec_name))
  return(this_sec_name)



### DB METHODS ###
#  
# CALLABLE: db_execute(my_stmt)
# CALLED BY: show_options()
# input: a SELECT statement (my_stmt)
# return: 
def db_execute(my_stmt):
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
  #print("DEBUG: did db_execute(my_stmt) lol")
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
    return("1")
  #print("DEBUG: did db_execute(my_stmt) lol")

### OPERATIONAL METHODS ####
#
# CALLABLE:
# CALLED BY show_options()
# input:
# return:
def list_sections():
  my_stmt = "SELECT * FROM sections;"
  execute_results = db_execute(my_stmt)
  line_ct=execute_results[0]
  rows=execute_results[1]
  print("DEBUG: line_ct is: " + str(line_ct))
  for line in rows:
    row0 = str(line[0])
    line1 = str(line[1])
    print("section " + row0 + ":  " + line1)
  #print("DEBUG: listed sections, lol")

#
# CALLABLE: check_for_section()
# CALLED BY: various
# input: user input 
# return: 0 or [id]
def check_for_section(this_sec_id):
  row0='0'
  #print("DEBUG: got an id: " + this_sec_id)
  this_stmt = "SELECT * FROM sections WHERE sec_id = " + this_sec_id + ";"
  #print("DEBUG: this_stmt is: " + this_stmt)
  count_and_rows = db_execute(this_stmt)
  result_count = count_and_rows[0]
  result_count = str(result_count)
  # if there are no rows, this will bypass
  print("DEBUG: there are " + result_count + " matches")
  for row in count_and_rows[1]:
    print("DEBUG: type(row):")
    print(type(row))
    row0 = row[0]
    row0 = str(row0)
    print("DEBUG: type(row0):")
    print(type(row0))
    print(row0)
    print("DEBUG: type(this_sec_id):")
    print(type(this_sec_id))
    print(this_sec_id)
    #line1 = str(line[1])
    #print("I got: section " + row0 + ":  " + line1)
    if row0 == this_sec_id:
      print("DEBUG: cool, row0 == this_sec_id, so row0 exists")
      return(row0)
  #print("DEBUG: returning row0: " + row0)
  #print(row0)
  sleep(1)
  return(row0)
  print("DEBUG: checked for section, lol")
#
# CALLABLE: 
# CALLED BY show_options()
# input: user input 
# return: FAIL or SUCCESS
def add_section():
  # get a section ID
  this_sec_id=get_confirm_sec_id()
  print("DEBUG: Ok, checking sec_id " + this_sec_id)
  # checking 
  rows=check_for_section(this_sec_id)
  rows0=int(rows[0])
  if rows0 > 0:
    print("DEBUG: not adding; rows[0] > 0; section exists")
    return("0")
  # confirm this_sec_name as input from get_confirm_sec_name()
  this_sec_name = get_confirm_sec_name()
  # this statement accepts this_sec_id and this_sec_name 
  # and returns hardcoded INSERT statement
  this_stmt = "INSERT INTO sections (sec_id,sec_name) VALUES (" + this_sec_id + ",'" + this_sec_name + "');"
  #print("DEBUG: statment is: " + this_stmt)
  is_success = db_interact(this_stmt) 
  # db_interact will return "1" if successful
  if is_success == "1":
    print("DEBUG: add_section succeeded")
  #print("DEBUG: Ok, rechecking sec_id for successful add:" + this_sec_id)
  new_rows=check_for_section(this_sec_id)
  rows0=str(new_rows[0])
  if rows0 == this_sec_id:
    print("DEBUG: confirmed add_section succeeded")
    return(rows0)
  else:
    quit()
  #print("DEBUG: this_stmt: " + this_stmt)
  print("DEBUG: tried to add section, lol")
#
# CALLABLE:
# CALLED BY: show_options()
# input:
# return:
def del_section():
  # get a section ID
  this_sec_id=get_confirm_sec_id()
  print("DEBUG: Ok, checking sec_id " + this_sec_id)
  # checking 
  rows=check_for_section(this_sec_id)
  rows0=str(rows[0])
  #print("DEBUG: rows0: " + rows0)
  #print("DEBUG: this_sec_id: " + this_sec_id)
  print(type(rows0))
  print(type(this_sec_id))
  if rows0 == this_sec_id:
    print("DEBUG: section exists; can be deleted")
  if rows0 != this_sec_id:
    print("DEBUG: section does not exist; returning")
    return("0")
  # this statement accepts this_sec_id and this_sec_name 
  # and returns hardcoded INSERT statement
  this_stmt = "DELETE FROM sections WHERE sec_id = '" + this_sec_id + "';"
  print("DEBUG del_section(): statment is: " + this_stmt)
  is_success = db_interact(this_stmt) 
  # db_interact will return "1" if successful
  if is_success == "1":
    print("DEBUG: del_section succeeded")
  else:
    return("0")
  #print("DEBUG: Ok, rechecking sec_id for successful add:" + this_sec_id)
  new_rows=check_for_section(this_sec_id)
  rows0=str(new_rows[0])
  # rows0 should be 0 if row is deleted
  if rows0 != this_sec_id:
    print("DEBUG: confirmed delete succeeded")
    return("1")
  else:
    return("0")
    quit()
  #print("DEBUG: this_stmt: " + this_stmt)
  print("DEBUG: tried to add section, lol")

# CALLABLE: show_options
# CALLED BY: main()
# input: user input
# return: list of options
# output: function()
def show_options():
  my_response = ''
  this_sec_id = "1"
  while my_response == '':
    clear()
    print("show_options:")
    print("0. list_sections")
    print("1. check_for_section(get_confirm_sec_id())")
    print("2. add_section")
    print("3. del_section")
    print("Q. quit")
    print("")
    my_response=input("Input: select option\n")
    print("")
    if my_response == "0":
      list_sections() #
    if my_response == "1":
      check_for_section(get_confirm_sec_id()) #
    if my_response == "2":
      add_section()
    if my_response == "3":
      del_section()
    if my_response == "q" or my_response == "Q":
      sys.exit()
    sleep(4)
    my_response = ''

def main():
  show_options()


############
############
main()
