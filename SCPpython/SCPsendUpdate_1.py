from paramiko import SSHClient
from scp import SCPClient
import os.path
import time
import sys
import paramiko
import pexpect

currentDir=sys.path[0]
#timestr = time.strftime("%H%M%S")
#os.makedirs(currentDir+"/BSversion"+timestr)
ipaddr1='192.168.5.11'
#ipaddr2='103'
status = True
while status:
	try:
		#print(ipaddr2)
		ssh_newkey = 'Are you sure you want to continue connecting'
		p=pexpect.spawn('scp -P 45296 '+currentDir+'/v1.1.0.6_fota.tar.gz guest@'+ipaddr1+':/tmp/')		#the command to scp update tar file
		i=p.expect([ssh_newkey,'password:',pexpect.EOF])
		if i==0:
			print ("I say yes")
			p.sendline('yes')
			i=p.expect([ssh_newkey,'Password:',pexpect.EOF])
		if i==1:
			print ("I give password",)
			p.sendline("guest")
			p.expect(pexpect.EOF)
		elif i==2:
			print ("I either got key or connection timeout")
			pass
		print (p.before)

	except:
		print(ipaddr1+': connection fail')
		pass
	#ipaddr2=str(int(ipaddr2)+1)

	time.sleep(1)
	ssh = SSHClient()
	ssh.load_system_host_keys()
	ssh.connect(hostname='192.168.5.11', 			#Need Changes if in different IP Addr
				port = '45296',
				username='guest',
				password='guest',
				)

	ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("tar -xzf /tmp/v1.1.0.6_fota.tar.gz -C /tmp")
	exit_code = ssh_stdout.channel.recv_exit_status() # handles async exit error
	ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("ls /tmp")
	exit_code = ssh_stdout.channel.recv_exit_status() # handles async exit error
	for line in ssh_stdout:
		print(line.strip())
	status = False
