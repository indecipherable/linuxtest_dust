#!/usr/bin/env bash
mysql -u root --password='my_password' --database='linuxquiztest' --execute='SHOW ENGINE INNODB STATUS;' | grep LATEST
