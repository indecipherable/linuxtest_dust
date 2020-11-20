import mysql.connector
from mysql.connector import errorcode
import sys
import re
import os
from os import listdir
from os.path import isfile, join
from os import walk
from pprint import pprint as p
import glob

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
q_dir=project_dir+"/questions/"
#print("DEBUG: q_dir is: %r" % q_dir)
# DEBUG: show properly parsed questions directory
#print("DEBUG: question_dir is: " + q_dir)
# Assign questions directory/*txt to this_glob
# DEBUG: show glob
#print("DEBUG: this_glob is: " + this_glob)

class FuzzException(Exception):
  print("DEBUG: FuzzException")

class IndexException(Exception):
  print("DEBUG: IndexException")


#def find_question_files():
##  f = []
#  question_count = 0
#  #print(glob.glob("/home/redmage/workspace/linuxtest_delta/questions/*txt"))
#  # this should be dynamic, not hardcoded
#  #g = glob.glob("/home/redmage/workspace/linuxtest_smoke/questions/*txt")
#  g = glob.glob(this_glob)
#  # i is a file in the glob of files
#  for i in g:
#    # question_count should give exact # of question files
#    question_count = question_count + 1
#    # select an arbitrary file to use
#    if question_count == 10:
##      print("DEBUG: arbitrary 10th file: " + i)
#      with open(i) as f:
#        content = f.readlines()
#        for line in content:
#          pass
#    else:
#      pass
#  return (question_count, g)
##  print("DEBUG: question count: %s" % question_count)

def get_column_values():
  pass
  #return (column_count, column_title_list, column_datatype_list, column_null_ok_list, column_is_key_list)

def database_insert(parsed_database,parsed_file):
  try:
    cnx = mysql.connector.connect(user='graymage', password='my_password',
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
    #cursor.execute("INSERT INTO [table] (%s %s)")
    my_columns = cursor.fetchall()
    my_stmt = "INSERT INTO question (......) VALUES (......)"
    my_data = ["3", 'Is the sky green', 'no', 'yes']
    my_stmt = "INSERT INTO questions (q_id, question, answer, wrong) VALUES (%s, %s, %s, %s)"
    cursor.execute(my_stmt, my_data)
    #cursor.executemany(my_stmt, my_data)

# for each index, validate a line:
def input_validation(column_datatype,column_null_ok,this_file_line,i):
  # EVALUATE COLUMNS
  print("")
  print("input_validation.DEBUG: column_null_ok is: %r" % column_null_ok)
  #print("input_validation.DEBUG: this_file_line is: %r" % this_file_line)
  this_file_line = strip_end(this_file_line, "\n")
  print("input_validation.DEBUG: this_file_line.strip() is: %r" % this_file_line)
  chr_ct = 0
  # by this point we are accepting a line sanitized of newline
  for i in this_file_line:
    chr_ct = chr_ct + 1
#        print("DEBUG: this file_line.chr_ct() fails db constraint")
#  print("DEBUG: Start input_validation ...")
#  print("DEBUG: Setting variables ...")
# # print("DEBUG: l, i are: %r %r" % (l, i))
  dt_ints = re.findall(r'\d+', column_datatype)
  dt_type = re.findall(r'\w+', column_datatype)
#  print("DEBUG: dt_ints is: %r" % dt_ints)
#  print("DEBUG: dt_type is: %r" % dt_type)
  # EVALUATE FILE LINES
  #print("DEBUG: this_file_line pre-strip is: \n%r" % this_file_line)
  #print("DEBUG: this_file_line post-strip is: \n%r" % this_file_line)
#  print("DEBUG: this_file_line type is str: %r" % this_is_str)
  # SYNTHESIZE
#  print("DEBUG: dt_type is: %r" % dt_type)
#  print("DEBUG: dt_type[0] is: %r" % dt_type[0])
#  print("DEBUG: variables OK")
#  for element in dt_type:
#    w = re.match("\w+", element)
#    if w:
#      print((w.groups()))
##      print("DEBUG: w is: %r" % w)
  # if the column can't be null, verify its length
  # if column is not null and meets length, pass
  if (column_null_ok == "NO") or (column_null_ok == "no"):
    #print("input_validation.DEBUG: chr_ct is: %r" % chr_ct)
    # test for a line more than 0 characters in length
    if chr_ct > 0:
      #print("input_validation.DEBUG: line character count > 0; pass")
    # test for a line no more than db specified length
      if chr_ct <= dt_ints:
	pass
        #print("input_validation.DEBUG: %r => line character count > 0; pass" % dt_ints)
      # test for a line of 0 or negative(?!) length
      else:
        raise FuzzException
    else:
      raise FuzzException
  if (column_null_ok == "yes") or (column_null_ok == "yes"):
    pass
    #if chr_ct == 0:
      #raise FuzzException
  if dt_type[0] == "varchar": # dt_type[0] is datatype title
#    print("DEBUG: chr_ct and dt_ints: %r %r" % (chr_ct, dt_ints[0]))
    # dt_ints[0] holds the cased length of the datatype
    dt_ints = int(dt_ints[0])
    # database constraint
#    print("DEBUG: column_null_ok is: %r" % column_null_ok)
    if dt_ints == 255:
      if chr_ct < dt_ints:
        pass
#        print("DEBUG: this_file_line passes db constraint; pass")
#        print("DEBUG: this_file_line is OK to input")
      else:
        pass
#        print("DEBUG: this file_line.chr_ct() fails db constraint")
        raise FuzzException
  if dt_type[0] == "timestamp":
    print("dt_type == timestamp")
  if dt_type[0] == "int":
    print("dt_type == INT")

# parse calls input_validation before returning
# mysql-friendly statements
# parse() should execute BY FILE
def parse(column_count,column_names,column_datatype_list,column_null_ok_list,column_is_key_list,this_file_line_count,this_file_line_list,i):
  print("parse.DEBUG: Starting parse ....")
  # this statically set variable offsets an integer for an index
  column_count_zero_index = column_count - 1
  file_line_zero_index = this_file_line_count - 1
###### get nonenterable column count ######
  key_count = 0 
  # for each column
  for i in range(0,column_count):
    #print("parse.DEBUG: column_is_key_list[i] is: %r" %column_is_key_list[i])
    if column_is_key_list[i] == "PRI":
      key_count += 1
    #print("parse.DEBUG: key_count is: %r" % key_count)
  timestamp_count = 0
  #for i in range(0,column_count_zero_index):
  for i in range(0,file_line_zero_index):
    #print("parse.DEBUG: column_datatype_list[i] is: %r" % column_datatype_list[i])
    if column_datatype_list[i] == "timestamp": # dt_type[0] is datatype title
      #print("parse.DEBUG: we got a timestamp")
      timestamp_count += 1
    #print("parse.DEBUG: timestamp_count is: %r" % timestamp_count)
  #print("parse.DEBUG: key_count is: %r" % key_count)
  #print("parse.DEBUG: timestamp_count is: %r" % timestamp_count)
  nonenterable_column_count = 0
  nonenterable_column_count += key_count 
  nonenterable_column_count += timestamp_count
  enterable_column_count = column_count - nonenterable_column_count
  #print("parse.DEBUG: nonenterable_column_count is: %r" % nonenterable_column_count)
  #print("parse.DEBUG: enterable_column_count is: %r" % enterable_column_count)
  #print("parse.DEBUG: have a range of (0,%r) for %r columns" % (nonenterable_column_count,column_count))
  # this for loop defines how we align the column names and file lines
  # nonenterable_column_count offsets the iterable index range to 0 
  #print("parse.DEBUG: this_file_line_count is: %r" % this_file_line_count)
  #print("parse.DEBUG: column_count is: %r" % column_count)
  #assert (this_file_line_count > column_count),"lines > columns!"
  if this_file_line_count > enterable_column_count:
      print("parse.DEBUG: Exception: file can overload DB")
      raise FuzzException()
  # i refers to column_count; this for loop keys to column_count
  for i in range(0,column_count): # operate on all columns
#    print("parse.DEBUG: i in column_names[i] is: %r" % column_names[i])
#    listzero = column_null_ok_list[0]
#    listone = column_null_ok_list[1]
#    print("DEBUG: column_null_ok_list[0]:" % listzero)
#    print("DEBUG: column_null_ok_list[1]:" % listone)
    try:
      # case for column_list index zero (id) and value assigned
      # by some other function
      if i == 0:
        print("parse.DEBUG: i == 0") 
        #input_validation(column_datatype_list[i],column_null_ok_list[i],i)
	print("parse.DEBUG: this_file_line_list[i] is: %r" % this_file_line_list[i])
        input_validation(column_datatype_list[i],column_null_ok_list[i],this_file_line_list[i],i)
      # cases for index count with values
      # if i > 0:
      if i > 0:
        print("parse.DEBUG: i > 0") 
        # only accepting files constrained to enterable_column_count
          # j offsets the index to account for index column value
          #print("parse.DEBUG: i is: %r" % i)
          j = i - 1
          #print("parse.DEBUG: j is: %r" % j)
	  if j < this_file_line_count:
            print("parse.DEBUG: i in column_names is: %r" % column_names[i])
            input_validation(column_datatype_list[i],column_null_ok_list[i],this_file_line_list[j],i)
  	  #print("parse.DEBUG: this_file_line_count is: %r" % this_file_line_count)
            #print("parse.DEBUG: line is: %r" % this_file_lines[j]) input_validation(column_datatype_list[i],column_null_ok_list[i],this_file_lines_list[j],i)
            #input_validation(column_datatype_list[i],column_null_ok_list[i],this_file_lines[j])
          if j == this_file_line_count:
  	    print("parse.DEBUG: Does something need to happen here?")
            input_validation(column_datatype_list[i],column_null_ok_list[i],this_file_line_list[j],i)
            #input_validation(column_datatype_list[i],column_null_ok_list[i],"")
            #input_validation(column_datatype_list[i],column_null_ok_list[i],this_file_lines[j])
            #print("parse.DEBUG: column_datatype_list[j] is: %r" % column_datatype_list[j])
    except IndexException: 
      print("parse.DEBUG: oops")
      #print("DEBUG: looks like I got no input for this_file_lines[%r]" % j)
### for i in range(0,enterable_column_count):
###     pass
#  for column_name in column_names:
#    print("DEBUG: column_name is: %r" % column_name)
#  for line in file_lines:
#    input_validation(line, index)
#    print("DEBUG: line is: %r" % line)
#    index += 1
  print("Generating database statements...")
  my_data = []
  my_data += i
  print("parse.DEBUG: my_data is: %r" % my_data)
  #my_data = ["3", 'Is the sky green', 'no', 'yes']
  my_stmt = []
  print("parse.DEBUG: my_stmt is: %r" % my_stmt)
  #my_stmt = "INSERT INTO questions (q_id, question, answer, wrong) VALUES (%s, %s, %s, %s)"

# main() gets column_count, column_name_list from get_columns()
def main():
  print("main.DEBUG: ")
  ## begin SQL querying
  ## SQL query should be available to main()
  try:
    cnx = mysql.connector.connect(user='graymage', password='my_password',
                                  host='127.0.0.1', database='linuxquiztest')
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
  cursor = cnx.cursor()
  cursor.execute("DESCRIBE questions;")
  my_columns = cursor.fetchall()
  cursor.close()
  ### end SQL querying
  ### begin assignment
  column_count = 0
  # for each column fetched to my_columns by cursor.fetchall()
  for a_column in my_columns:
    # debug to show column_count
    #print("DEBUG: column_count is: %r % column_count)
    # increment
    column_count += 1
  # instantiate column_name_list with arbitrary number of columns
  #print("DEBUG: Column_count is: %r" % column_count)
  column_title_list = [[]] * column_count
  column_title_string = ""
  column_datatype_list = [[]] * column_count
  column_null_ok_list = [[]] * column_count
  column_is_key_list = [[]] * column_count
  column_count = 0
  #print("DEBUG: column_name_list is: %r" % column_name_list)
  for a_column in my_columns:
    #print("DEBUG: Column_list is: %r" % column_name_list)
    # assign get_columns[index] to column_name_list[index]
    #print("DEBUG: a_column[0] is: %r" % a_column[0])
    column_title_list[column_count] = a_column[0]
    #print("DEBUG: a_column[1] is: %r" % a_column[1]) # datatype
    column_datatype_list[column_count] = a_column[1]
    #print("DEBUG: a_column[2] is: %r" % a_column[2]) # is_required
    column_null_ok_list[column_count] = a_column[2]
    #print("DEBUG: a_column[3] is: %r" % a_column[3])
    column_is_key_list[column_count] = a_column[3]
    #print("DEBUG: a_column[4] is: %r" % a_column[4])
    # increment column_count
    column_count += 1
  column_count_zero_index = column_count - 1
  for i in range(0,column_count_zero_index):
    if i <= (column_count_zero_index):
      column_title_string += column_title_list[i] + ","
    if i > (column_count_zero_index):
      column_title_string += column_title_list[i] 
    else: 
      column_title_string += column_title_list[i] 
    print("main.DEBUG: column_title_string is: %r" % column_title_string)
  # Operate on files in glob
#  for i in question_glob:
  #    # DEBUG: enumerate items in glob
  #    print("DEBUG: glob_file is: %r" % i)
  #    DEBUG: i is an element of glob
  this_glob=(q_dir+"*txt")
  question_glob = glob.glob(this_glob)
  q10 = question_glob[10]
  i=q10
#  q10_line_count = 0
  print("question_glob[10] is: %r" % question_glob[10])
  print("DEBUG: i is: %r" % i)
  # Assume a file has 0 lines
  this_file_line_count = 0
  # for each file in file or glob:
  #for i in question_glob: 
  with open(i) as f:
    content = f.readlines()
    # this routine confirms file line count in a file
    for line in content:
      # increment this_file_line_count per line
      this_file_line_count  += 1
      # DEBUG: print a line in content from file opened
      #print("DEBUG: line is: %r" % line)
    # this_file_line_count is given by above this_file_line_count
  this_file_line_list = [[]] * this_file_line_count  
  # line_id is index of list
  line_id = 0
  # this populates 
  for line in content:
    this_file_line_list[line_id] = line
    # increment line_id per line
    line_id += 1
    # DEBUG: showing this_file_line_list[3] is properly populated
    #print("DEBUG: this_file_line_list[3] is: %r" % this_file_line_list[3])
  try:
    #print("main.debug shows column_count: %r" % column_count) 
    #print("DEBUG: column_datatype_list[0] is: %r" % column_datatype_list[0])
    parse(column_count,column_title_list,column_datatype_list,column_null_ok_list,column_is_key_list,this_file_line_count,this_file_line_list,i)
  except FuzzException:
    print("Halting for FuzzException; see file: \n%r" % i)
    #pass
  
#main(get_columns())
# main(get_column_values(),find_question_files()) calls get_column_values()
# and find_question_files()
# get_column_values() returns: (column_count, column_title_list, column_datatype_list, column_null_ok_list)
# find_question_files() returns: (question_count, g) # g is a glob
main()
