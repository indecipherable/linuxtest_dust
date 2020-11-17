# works as intended
import sys
import mysql.connector

cnx = mysql.connector.connect(user='root', password='nice_password',
                                host='127.0.0.1', database='linuxquiztest')
cnx.close()
