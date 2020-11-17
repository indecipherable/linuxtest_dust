#!/usr/bin/env bash
#mysql -u root --password='my_password' --database='linuxquiztest' --execute='DESCRIBE questions;'
#j=0

#q0="insert into questions (q_id, question, correct_a, incorrect_1, incorrect_2, incorrect_3, incorrect_4, created_at) values ("

#q1=""
#queueone=""
#q2=")"

#echo "DEBUG: addexpr = $addexpr"
#cat q_01.txt | while read aline; do  j=$(( $j + 1 )) && echo $j && echo $aline; done
#cat q_01.txt | while read aline; do echo "DEBUG: aline is: $aline"; done
#cat q_01.txt | while read aline; do q1=$(echo $q1, $aline) && echo "DEBUG: q1 is: $q1"; done
#cat q_01.txt | while read aline; do q1=$(echo $q1, $aline); done; echo "DEBUG: q1 is: $q1"
#cat q_01.txt | while read aline; do queueone=$(echo "$queueone, $aline"); done 
#cat q_01.txt | while read aline; do queueone=$(echo "$queueone, $aline"); done; \
#  echo "DEBUG: queueone is: $queueone"
#echo "DEBUG: q1 is: $q1"
#echo "DEBUG: queueone is: $queueone"
#queueone=$(cat q_01.txt)
#queuearray=($(cat q_01.txt | while read aline; do echo $aline; done))
#echo "DEBUG: queueone is: $queueone"
#cat q_01.txt | while read aline; do echo $aline; done # this echos lines
#echo "DEBUG: queueone is: $queueone"
#cat q_01.txt | while read aline; do queueone="$queueone, $aline"; done
#echo "DEBUG0: queueone is: $queueone"
#cat q_01.txt | while read aline; do queueone="$queueone $aline, "; done
#echo "DEBUG1: queueone is: $queueone"
#cat q_01.txt | while read aline; do queueone="$queueone, $aline, "; done

#echo "DEBUG2: queueone is: $queueone"
#echo $queueone
#echo "DEBUG: queuearray is: ${#queuearray[*]}" #echo $q0
#echo $queueone
#echo $q2

#echo "DEBUG: addexpr = $addexpr"
this_command=$(python ./010_add_entry.py)
echo $this_command
