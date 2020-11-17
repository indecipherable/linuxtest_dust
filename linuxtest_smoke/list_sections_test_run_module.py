# works as intended
import mysql.connector
from mysql.connector import errorcode
import sys
import re
import os
from os import system, name 
from pprint import pprint as p
from time import sleep
import list_sections

sections=list_sections.main()
#for i in sections[1]:
#  print(i)
print("DEBUG: line_count:")
#print(line_count)
print(sections[0])
