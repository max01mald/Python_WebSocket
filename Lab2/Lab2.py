Laimport socket 
import os
import shutil

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
		
def server():
	
	https = parseCommand()
	
	#https = httpfs(1,8080,"/Users/Max/Desktop")
	
	get = 0
	post = 0
	contents = 0
	
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	 
	serverSocket.bind((https.host , https.port))
	serverSocket.listen(1)

	print("The server is ready to receive") 
	
	while 1:	
		connectionSocket, addr = serverSocket.accept() 
		
		sentence = connectionSocket.recv(1024).decode("utf-8") 
		
		if sentence[0:3] == "GET":
			get = 1
		
		if sentence[0:4] == "POST":
			post = 1
		
		find = Find(sentence)
		
		
		try:
			if get == 1:
				if find[0] == "/":
					if len(find)> 5:
						if find[4] != "?":
							contents = List(https)
						else:
							contents = Contents(https, find[5:len(find)],1)
					else:
						contents = List(https)
				elif find == "/.":
					contents = prevDir(https)
				else:
					print(find)
					contents = Contents(https, find[5:len(find)],1)
		
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
		
			contents = bytes(contents,'utf-8')
			connectionSocket.send(contents)

		except ValueError:
			print("Error")
		except TypeError:
			print("Error")
			
		connectionSocket.close()
		
		

server()


'''
httpfs -v -p 8080 -d /Users/

httpc GET -p 8080 http://localhost/get
httpc GET -p 8080 http://localhost/get?test
httpc GET -p 8080 http://localhost/get?tester


httpc POST /quick -d 'Wowa' -p 8080 http://localhost

httpc post -h Content-Type:application -d '{"Assignment": 1}' http://httpbin.org/post 


'''









