import paramiko

username = "guest"
password = "guest"
ip = "192.168.5.11"
port = "45296"

ssh_client = paramiko.SSHClient()
ssh_client.connect(hostname=ip,username=username,password=password,port=port)
