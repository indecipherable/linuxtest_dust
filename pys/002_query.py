# works as intended
import sys
import mysql.connector

def main():
  # instantiates a sql connection object 'cnx'
  cnx = mysql.connector.connect(user='root', password='nice_password',
                                  host='127.0.0.1', database='linuxquiztest')
  # instantiates a connection cursor object 'cursor'
  cursor = cnx.cursor()
  query = ("SHOW databases;")
  #query = ("SELECT * from questions;")
  #q_id = 
  cursor.execute(query, params=None, multi=False)
  databases = cursor.fetchall()
  for a_database in databases:
    print(a_database)
  cursor.close()
  cnx.close()
  return databases

main()
