#!/usr/bin/python
# PURPOSE:
# This tool is designed to take a given script and append echoes
# and stdout redirects into a target file. This enables us to quickly
# (and somewhat manually) reconstruct the script on
# a target machine without needing to transfer the script over.

target_to_echo = raw_input("enter full path to file ")
destination_file = raw_input("where should the echoes redirect? ")
try:
    for line in open(target_to_echo, 'r'):
        print("echo \'" + line.rstrip() + "\' >> " + destination_file)

except:
    print "try again, something went wrong (typo in your inputs?)"

