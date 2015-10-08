import socket, pickle , select
import sys
from sys import exit

sockToServer=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockToServer.connect((sys.argv[1],9908))
sockForClients=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#we cant call more than one instance of program due to bind on port 6666
sockForClients.bind(('0.0.0.0',6666))
sockForClients.listen(20)
global bd
global myHost
print ("Connected to master")
myHost=[(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
while 1:
	rfds, wfds, efds = select.select( [sys.stdin,sockForClients,sockToServer], [], [], .1)		
	for sock in rfds:		
		if sock == sys.stdin:		
			write = sys.stdin.readline()
			read=write[:5]
			quit="/quit"
			Quit="/Quit"
			if read == quit or write == Quit:
				sockToServer.send(bytes("ENDCONN","utf-8"))		
				sockToServer.close()
				sockForClients.close()
				print ("Exiting....")
				print ("bye")
				exit()
			else :
				for i in bd:
					if i != myHost:
						socketMsg=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						socketMsg.connect((i,6666))
						socketMsg.send(bytes("<"+myHost+">"+write,"utf-8"))
						socketMsg.close()
		elif sock == sockForClients:
			nS,(nh,nP)=sockForClients.accept()
			codeMsg=nS.recv(4096)
			msg=codeMsg.decode("utf-8")
			print (msg)
			nS.close()
		elif sock == sockToServer:
			try:
				bd_s=sockToServer.recv(4096)
				bd=pickle.loads(bd_s)
			except:	
				pass




