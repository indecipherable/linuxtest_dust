import sys
import re
import os
from pprint import pprint as p

def find_where_am_i():
  # reads q_00.txt and inputs lines to database
  def strip_end(text, suffix):
    if not text.endswith(suffix):
      return text
    return text[:len(text)-len(suffix)]
  
  # enumerate where our project directories are
  print("DEBUG: sys.path is: %r" % sys.path)
  py_wd=os.getcwd()
  print("DEBUG: py_wd is: %r" % py_wd)
  project_dir=strip_end(py_wd, "/pys")
  print("DEBUG: project_dir is: %r" % project_dir)
  q_dir=project_dir+"/questions"
  print("DEBUG: q_dir is: %r" % q_dir)

