from packet import Packet
import socket 
import os
import shutil
from math import ceil
from multiprocessing import Process, Event

NL = "\r\n"
DL = "\r\n\r\n"

class httpfs:
	
	def __init__(self, verbose, port, path):
		
		self.verbose = int(verbose)
		self.port = port
		self.host = "127.0.0.1"
		
		working = os.path.dirname(os.path.realpath(__file__))
		size = len(working)
		
		i = 0
		
		while i < len(path):
			if path[i:size] == working:
				self.path = path
				break
			else:
				print("This directory is not in the scope of the server\nDefault Root is Path")
				self.path = working
				break
			i += 1
		
		
		
		return
	
	def prnt(self):
		print("V: " + str(self.verbose))
		print("Host: " + self.host)
		print("Port: " + str(self.port))
		print("Path: " + self.path)


def findEnd(string):
	i = 0
	count = 0
	start = 0
	end = len(string)
	
	while i < len(string):
		if string[i] == " ":
			count += 1
			if count == 1:
				start = i+1
			if count == 2:
				end = i
		i += 1
		
	return string[start:end]
		
		
def parseCommand():
	i = 0
	verbose = 0
	port = 80
	path = "/"
	
	command = input("$Server: ")
	
	while i < len(command):
		if command[0:6] != "httpfs":
			command = input("Error please enter new command: ")
			i = 0
		
		if command[i] == "-" and i+1 != len(command):
			if command[i+1] == "v":
				verbose = 1
			if command[i+1] == "p":
				port = int(findEnd(command[i+1:len(command)]))
			if command[i+1] == "d":
				path = findEnd(command[i+1:len(command)])
		i += 1
		
	request = httpfs(verbose, port, path)
	
	return request

	
def Directory(httpfs):

	dir_path = httpfs.path
	
	if httpfs.verbose == 1:
		print("Current Working Directory " + dir_path)
	
	all_files = os.listdir(dir_path)
	
	return all_files
	

def prevDir(httpfs):

	dir_path = httpfs.path
	
	if httpfs.verbose == 1:
		print("Current Working Directory " + dir_path)
	
	i = len(dir_path)-1
	
	while i > 0:
		if dir_path[i] == "/" and i != len(dir_path)-1:
			dir_path = dir_path[0:i]
			break
		i -= 1
	
	working = os.path.dirname(os.path.realpath(__file__))
	size = len(working)
		
	i = 0
	
	while i < len(dir_path):
		if dir_path[i:size] == working:
			break
		elif dir_path[i:size] != working:
			print("This directory is not in the scope of the server\nDefault Root is Path")
			dir_path = working
			break
		i += 1
	
	return dir_path 
	
		
def List(httpfs):	
	
	all_files = Directory(httpfs)
	
	text = []
	folder = []
	
	for files in all_files:
	
		i = 0
		file = 0
		
		while i < len(files):
			if files[i] == ".":
				file = 1
			i += 1
		
		if file == 1:
			if files != "Lab2.py":
				text.append(files)
		else:
			folder.append(files) 	
	
	texts = "List of Text Files in Current Working Directory\n" + '\n'.join(text)
	folders = "List of Folders in Current Working Directory\n" + '\n'.join(folder)
	
	package = "\n" + texts + "\n" + folders + "\n"
	
	return package
	

def Contents(httpfs, find, over):
	
	directory = Directory(httpfs)
	size = len(find)
	handle = ""
	content = ""
	exit = 0
	
	for files in directory:
		i = 0
		
		if exit != 1:
			while i < len(files):
				if files[i:size] == find:
					print("root " + find)
					print("ext " + files[size:len(files)])
					if files[size:len(files)] == ".txt":
						f = open(find + ".txt", "r")
						content = "File Contents of " + find + ".txt\n" +f.read()
						f.close()
						exit = 1
						break
					elif files[size:len(files)] == "":
						httpfs.path += "/" + find
						content = "New Working Directory " + httpfs.path
						exit = 1
						break
				else:
					content = "404"
			
				i += 1
		else:
			break
				
	return content


def Create(httpfs, find, over, body):
	
	directory = Directory(httpfs)
	size = len(find)
	handle = ""
	content = ""
	exit = 0
	
	for files in directory:
		i = 0
		
		if exit != 1:
			while i < len(files):
				#print("1"+find+"1")
				if files[i:size] == find:
					if files[size:len(files)] == ".txt":
						if over == 1:
							f = open(find + ".txt", "w")
							f.write(body)
							content = "File Contents of " + find + ".txt is modified\n"
							f.close()
							exit = 1
							break
						else:
							content = "File Contents of " + find + ".txt cannot be modified\n"
							exit = 1
							break
					elif files[size:len(files)] == "":
						if over == 1:
							shutil.rmtree(httpfs.path + "/" + find)
							os.mkdir(httpfs.path + "/" + find)
							content = "New Folder " + find
							exit = 1
							break
						else:
							content = "Folder " + find + " cannot be modified\n"
							exit = 1
							break
				else:
					f = open(find + ".txt", "w")
					f.write(body)
					f.close()
				i += 1
		else:
			break
				
	return content
	
def Find(string):
	i =0
	count = 0
	while i < len(string):
		if string[i] == "/":
			count += 1
			if count == 2:
				return string[i:len(string)]
		i += 1

def FindLine(string):
	i =0
	
	print(string)
	while i < len(string):
		if string[i] == "\n":
			return i
		i += 1

def FindQ(string):
	i =0
	
	print(string)
	while i < len(string):
		if string[i] == "?":
			return i
		i += 1
		
def FindE(string):
	i =0
	
	print(string)
	while i < len(string):
		if string[i] == "=":
			return i
		i += 1

#===== MULTI =============================================================================

def task(event,conn,port):
	proc_id = os.getpid()
	event.wait()
	#print('timestamp of process id {}: {}'.format(proc_id, time.time()))
	hand_shake(conn,port)
		
	num_pkt = size(conn,port)
	
	data = select_repeat(conn,port,num_pkt)
	
	fin(conn,port,https,data)

#=========================================================================================

		
def server():
	
	https = parseCommand()
	
	demands = []
	processes =[]
	checking = 0
	
	#=== TCP CONNECTION === serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	conn.bind(('' , https.port))
	
	#=== TCP CONNECTION === serverSocket.listen(1)

	print("The server is ready to receive\n") 
	
	while 1:	
		#=== TCP CONNECTION === connectionSocket, addr = serverSocket.accept() 
		
		#=== TCP CONNECTION ===sentence = connectionSocket.recv(1024).decode("utf-8") 
		
		'''sentence, sender = conn.recvfrom(1024)
		
		p = Packet()
		p.decode(sentence)
		print(p.PeerPortNumber)
		print(sender)
		
		port = p.PeerPortNumber
		
		if port not in demands:
			demands.append(port)
		else:
			checking +=1 
			
		if checking == 2:
			break
			
		event = Event()
		
		i = 0
		
		while i <len(demands):
			print(demands[i])
			p = Process(target=task,args=(event,conn,demands[i]))
			processes.append(p)
			p.start()
			
			i += 1
		
		event.set()'''
		port = hand_shake(conn)
		
		num_pkt = size(conn,port)
		
		data = select_repeat(conn,port,num_pkt)
		
		fin(conn,port,https,data)
		
		
			
	conn.close()

def process(conn,https,sentence):
	get = 0
	post = 0
	
	print("SENTENCE\n" + sentence )
	if sentence[0:3] == "GET":
			get = 1
		
	if sentence[0:4] == "POST":
		post = 1
	
	find = Find(sentence)
	
	print("G: " + str(get))
	print("P: " + str(post))
	print("F: " + find)
	
	try:
		if get == 1:
			if find[0] == "/":
				if len(find) == 1:
					contents = List(https)
				else:
					print("HEREHER")
					contents = Contents(https, find[1:len(find)-4],1)
			elif find == "/.":
				contents = prevDir(https)
	
		if post == 1:
			split = FindLine(find)
			print(split)
			data = find[split+1:len(find)]
			find = find[1:split-1]
			
			contents = Create(https, find, 1, data)
	
		if https.verbose == 1:
			print("\nAddress: " + str(addr))
			print("\nServer Received: " + sentence)
			print(contents)
	
		if contents == "404":
			contents = "HTTP ERROR 404"
		else:
			contents = "HTTP OK 200\n" + contents
	
		return contents
		

	except ValueError:
		print("Error")
	except TypeError:
		print("Error")

def hand_shake(conn):
	
	ack = 0
	seq = 0
	
	state = ""
	p = Packet()
	
	timeout = 60
	timeout2 = 5
	
	while state != "ESTABLISHED":
		
		try:
			sentence, sender = conn.recvfrom(1024)
			
			conn.settimeout(timeout)
			p = Packet()
			p.decode(sentence)
			p.prnt()

			port = p.PeerPortNumber
			ack = int(p.SequenceNumber) + 1
		
		except socket.timeout:
			print("Wating for initiated Hand Shake\n")
		
		if p.PacketType == "SYN":		
			try:
				p.encode("SYN-ACK",seq,"127.0.0.1",port,str(ack))
				conn.sendto(p.to_send(), sender)
				conn.settimeout(timeout2)
			except socket.timeout:
				print("Timeout Expired in Sending SYN: " + str(timeout) + "s\n")		
			
		if p.PacketType == "ACK":
			seq = int(p.Payload)+1
		
			state = "ESTABLISHED"
			print(state + "\n")
	return port
		
def size(conn,port):
	
	timeout = 5
	
	try:	
		sentence, sender = conn.recvfrom(1024)
	
		p = Packet()
		p.decode(sentence)
		p.prnt()
	
		num = int(p.Payload)
		#port = p.PeerPortNumber
	
		p.encode("ACK",p.SequenceNumber,"127.0.0.1",port,str(num))
		conn.sendto(p.to_send(), sender)
		conn.settimeout(timeout)
		
		print("Size received: " + str(num) + "\nInitializing Buffer\n")
	
	except socket.timeout:
		print("Timeout Expired in size:  " + str(timeout) + "s\n")
				
	return num


def select_repeat(conn,port,num):
	
	i = 0
	i_w = 0
	ack = 0
	seq = 0
	
	N = int(ceil(num / 1013))
	
	window_base = 0
	window_width = int(N / 2)
	window_edge = window_width
	
	print(N)
	print(int(N/2))
	
	receive_buffer = [""] * int(N / 2)
	
	print(receive_buffer)
	
	data = []
	
	timeout = 5
	t = 0
	while window_base < N:
		
		while i < window_edge:
			
			try:
				sentence, sender = conn.recvfrom(1024)
				
				p = Packet()
				p.decode(sentence)
				p.prnt()
				
				ack = p.SequenceNumber
				#port = p.PeerPortNumber
				
				receive_buffer[ack%window_width] = p.Payload
				
				
				
				p.encode("ACK",seq,"127.0.0.1",port,str(ack))
				conn.sendto(p.to_send(), sender)
								
				if ack == window_width -1 and '' in receive_buffer:
					break
				elif '' not in receive_buffer:
					break
				
				print(i)
				print(ack)
				print(receive_buffer)
				
				
			except socket.timeout:
				print("Timeout Expired in size:  " + str(timeout) + "s\n")
				print(len(receive_buffer))
				
		while receive_buffer[window_base%window_width] != "":
			
			data.append(receive_buffer[window_base%window_width])
			
			receive_buffer[window_base%window_width] = ""
			window_base += 1
			window_edge = window_base + window_width
			
			print(window_edge)
			print("INSSISIFIJSDIOFJDZLF")
			if window_edge > N:
				window_edge = N
				
			print(window_base)
			print(window_edge)

	
	return data
	
	
def fin(conn,port,https,data):
	
	status = ""
	timeout = 5
	print("BEGINNN")
	print(data)
	
	while status != "PENDING":
		
		try:
				sentence, sender = conn.recvfrom(1024)
				
				p = Packet()
				p.decode(sentence)
				p.prnt()
				
				ack = p.SequenceNumber
				#port = p.PeerPortNumber
				
				
				if p.PacketType == "Data":
					data[6] = p.Payload
					
					p.encode("ACK",0,"127.0.0.1",port,str(ack))
					conn.sendto(p.to_send(), sender)
					
				if p.PacketType == "FIN":	
					p.encode("Data",0,"127.0.0.1",port,process(conn,https,"".join(data[len(data)-1])))
					conn.sendto(p.to_send(), sender)
					
					p.encode("ACK",0,"127.0.0.1",port,"")
					conn.sendto(p.to_send(), sender)
					
					
					status = "PENDING"
					print(status + "\n")
					
					
		except socket.timeout:
			print("ERRR")
			
	while status != "TERMINATED":
		
		try:
				p.encode("FIN",0,"127.0.0.1",port,"")
				conn.sendto(p.to_send(), sender)
				
				status = "TERMINATED"
				print(status + "\n")
				
				sentence, sender = conn.recvfrom(1024)
				
				p = Packet()
				p.decode(sentence)
				p.prnt()
				
		except socket.timeout:
			print("NO ACK\n")
	
	
	return "".join(data[len(data)-1])

server()


'''
httpfs -v -p 8080 -d /Users/

httpc GET -p 8080 http://localhost/get
httpc GET -p 8080 http://localhost/get?test
httpc GET -p 8080 http://localhost/get?tester


httpc POST /quick -d 'Wowa' -p 8080 http://localhost

httpc post -h Content-Type:application -d '{"Assignment": 1}' http://httpbin.org/post 


'''









