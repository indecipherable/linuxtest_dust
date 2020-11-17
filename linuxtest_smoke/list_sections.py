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
#  
# CALLABLE: db_select(my_stmt)
# CALLED BY: 
# input: a non-SELECT statement (my_stmt)
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
  #print("DEBUG: did db_execute(my_stmt) lol")
    return(line_ct,my_rows)

### OPERATIONAL METHODS ####
#
# CALLABLE:
# CALLED BY show_options()
# input:
# return:
def list_sections():
  my_stmt = "SELECT * FROM sections;"
  select_results = db_select(my_stmt)
  line_ct=select_results[0]
  rows=select_results[1]
  print("DEBUG: line_ct is: " + str(line_ct))
  for line in rows:
    row0 = str(line[0])
    line1 = str(line[1])
    #print("section " + row0 + ":  " + line1)
  #print("DEBUG: listed sections, lol")
  return(select_results)

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
  select_results=list_sections()
  return(select_results)


############
############
main()
