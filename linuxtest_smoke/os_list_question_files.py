# works as intended
import glob
import os

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
q_dir=project_dir+"/questions/"
#print("DEBUG: q_dir is: %r" % q_dir)

def find_question_files():
  f = []
  question_count = 0
  # defines the glob as question directory + *txt
  this_glob=(q_dir+"*txt")
  # this should be dynamic, not hardcoded
  g = glob.glob(this_glob)
  for i in g:
    question_count = question_count + 1
    print(i)
  print("DEBUG: question count: %s" % question_count)
  return (question_count,g)

find_question_files()
