import sys
import re
import os
from pprint import pprint as p
# trying to import where_am_i as module
#import importlib
#where_am_i="/000_where_am_i"
#sys.path.append(os.getcwd())
#import 000_where_am_i
#pm = __import__(where_am_i)
#find_where_am_i()


# defines strip_end for project_dir
def strip_end(text, suffix):
    if not text.endswith(suffix):
        return text
    return text[:len(text)-len(suffix)]
# enumerate where our project directories are
#print("DEBUG: sys.path is: %r" % sys.path)
py_wd=os.getcwd()
#print("DEBUG: thiscwd is: %r" % py_wd)
project_dir=strip_end(py_wd, "/pys")
#print("DEBUG: stripcwd is: %r" % project_dir)
q_dir=project_dir+"/questions"
#print("DEBUG: q_dir is: %r" % q_dir)

def entry_generator(my_file):
  # These are counters
  j=int(0)
  # this is the test file
  #print("DEBUG: this my_file is: %r" % my_file)
  # question realpath is question_dir + question
  my_file=q_dir + "/%r" % my_file
  my_file=re.sub('[\']', '', my_file)
  print("this my_file is: %r" % my_file)

  # THIS NEEDS TO QUERY THE DB FOR KEYS
  # RATHER THAN FLAT KEYS DEFINED HERE:
  # question_0 gives keys statically:
  my_stmt="INSERT INTO questions (sec_id, question, correct_a, incorrect_1, incorrect_2, incorrect_3, incorrect_4) values (%s, %s, %s, %s, %s, %s, %s)"
  #insert into questions (sec_id, question, correct_a, incorrect_1, incorrect_2, incorrect_3, incorrect_4) VALUES ('00', 'Did we put mattress under?', 'Mr Benson', 'Jerry', 'Beth', 'Redgrint', '');
  # question 1 stores values
  my_data0=""
  # n = number of lines
  n = sum(1 for line in (open(my_file)))
  ###print("DEBUG: Number of lines: %r") % n
  with open(my_file) as f:
    content = f.readlines()
    #print content
    content = [x.strip() for x in content]
    #print content
  # i is a line
  for i in content:
    j+=1
    if j == 1:
      my_data0 = "('" + i + "', "
    elif j > 1 and j < n:
      my_data0 = my_data0 + "'" + i + "', "
    else:
      my_data0 = my_data0 + "'" + i + "')"
  my_questiontotal = my_stmt+my_data0
  print("DEBUG: my_questiontotal is: \n%r" % my_questiontotal)

entry_generator("0101.txt")

