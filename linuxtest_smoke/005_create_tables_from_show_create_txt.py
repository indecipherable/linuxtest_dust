# works as intended
#
# takes flat file configuration from
# ../section_statements/[database].txt
# to create tables in target database
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

# NOTE - this function does not test for existence!!
# NOTE - this function needs better logic!!
def create_tables(content):
  try:
    cnx = mysql.connector.connect(user='root', password='nice_password',
                                  host='127.0.0.1', database='linuxquiztestdev')
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
    raise
  else:
#    print content
    cursor = cnx.cursor()
    try:
      cursor.execute(content, params=None, multi=False)
    except mysql.connector.Error as err:
      if err.errno == mysql.connector.IntegrityError:
        print("oopsie")
    cursor.close()
    cnx.commit()
    cnx.close()
    print("create_tables succeeded probably!")

def main():
  g = glob.glob(this_glob)
  pat = re.compile(r"\b\|\w*\w\b\|")
  for a_file in g:
    file_lines = []
    print(a_file)
    with open(a_file) as f:
      #content = f.readlines()
      content = f.read()
      #for a_line in content:
      content = content.rpartition("| ")[2]
      content = re.sub(r' \|','',content)
      #print line
      #print content.rstrip("\n")
      #if re.search(line,"|"):
      #  print "found it!"
      #pass
      create_tables(content)

main()
