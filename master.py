import socket , pickle , select , sys

sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#sock.setblocking(0)
#sock.settimeout(1)
sock.bind(('0.0.0.0',9908))
sock.listen(5)
print ("Master server launched")
sockList=[]
list=[]
while 1:
	try:
		newS,newP=sock.accept()
		sock.settimeout(.1)
		host,port=newS.getpeername()
		print (host+" connected")	
		sockList.append(newS)
		list.append(host)
#each time somebody connect we send everybody the new users list
		data=pickle.dumps(list)
		for i in sockList:
			i.send(data)
	except: 
		pass
	
	readdable,writeable,error=select.select(sockList,[],[],.1)
	if readdable:	
		for i in readdable:				
			h,p=i.getpeername()			
			endConnbytes=i.recv(1024)
			if endConnbytes:			
				endConn=endConnbytes.decode("utf-8")
				if endConn == "ENDCONN":
					sockList.remove(i)	
					list.remove(h)
					print (h+" disconnected")
					print ("Sending new contact list")
					data=pickle.dumps(list)
					for j in sockList:
						j.send(data)
	
	print("---contact list---")
	for i in list:
		print (i)
#managing program close	
	rfds, wfds, efds = select.select( [sys.stdin], [], [], .1)
	if rfds:
		write = sys.stdin.read(5)
		sock.close()
		print ("Exiting ...")
		sys.exit(0)
