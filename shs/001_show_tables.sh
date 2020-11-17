#!/usr/bin/env bash
#mysql -u root --password='my_password' --database='linuxquiztest' --execute='SHOW TABLES;'
mysql -u root --password='my_password' --database='linuxquiztest' --execute='DESCRIBE questions;'
