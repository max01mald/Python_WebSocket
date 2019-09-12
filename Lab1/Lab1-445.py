
import socket 

NL = "\r\n"
DL = "\r\n\r\n"

class httpc:
	
	def __init__(self, status, port, func, verbose, headers, data, input, type, url, output, f_query):
		self.status = status
		self.func = func
		self.verbose = int(verbose)
		self.headers = headers
		self.data = data
		self.input = input
		self.type = type
		self.url = url
		self.output = output
		self.host = ""
		self.ext = ""
		self.f_query = f_query
		
		if str(port) != "-1":
			self.port = int(port)
		else:
			self.port = 80
			
		if type == 2:
			f = open(input, "r")
			self.in_data = f.read()
			f.close()
		return
	
	def prnt(self):
		print("Status: " + str(self.status))
		print("V: " + str(self.verbose))
		print("Func: " + self.func)
		print("H:")
		print(self.headers)
		print("D: " + self.data)
		print("F: " + self.input)
		print("T: " + str(self.type))
		print("O: " + self.output)		
		print("URL: " + self.url)
		print("Host: " + self.host)
		print("Port: " + str(self.port))
		print("Ext: " + self.ext)
		print("FQ: " + self.f_query)

def delimit(string):
	i = 0
	count = 0
	list = []
	
	end = len(string)
	
	while i < end:
		if ord(string[i]) == 34:
			list.append(i)
		i+=1
	
	for i in list:	
		insert = ""
		string = string[0:i+count] + insert + string[i+count:len(string)]
		count += 1
			
	return string
	
def findEnd(string):
	i = 0
	
	if string == "":
		return 0
	while string[i] != " ":
		i += 1
		if i == len(string):
			return i
	return i

def findSlash(string):
	i = 0
	
	if string == "":
		return 0
	while string[i] != "/":
		i += 1
		if i == len(string):
			return i
	return i
	
def findClose(string):
	i = 0
	
	if string == "":
		return 0
	while string[i] != "}" and string[i+1] != "'":
		i += 1
		if i == len(string):
			return i
	return i+1
	
def urlParse(httpc):
	i = 0
	url = httpc.url
	
	if url == "":
		return 0
	if url[i:i+7] != "http://":
		return 0
		
	i = findSlash(url[7:len(url)])
	httpc.host = url[7:7+i]
	httpc.ext = url[7+i:len(url)]
	
	if httpc.ext != "":
		if httpc.ext[len(httpc.ext)-1] == "'":
			httpc.ext = httpc.ext[0:len(httpc.ext)-1]
	
def commandParse(command):
	i = 0
	status = 1
	type = 0
	verbose = 0
	data = ""
	func = ""
	input = ""
	output = ""
	url = ""
	port = "-1"
	f_query = ""
	headers = []
	
	while i < len(command):
		
		if command[0:5] != "httpc":
			status = 0
		
		if command[6:9] == "get" or command[6:9] == "GET":
			func = "GET "
		elif command[6:10] == "post" or command[6:10] == "POST":
			func = "POST "
		elif command[6:10] == "help":
			j = findEnd(command[11:len(command)])
			func = command[11:11+j]
			status = 2
		else:
			status = 3
		
		if command[i] == "/" and command[i+1] != "/" and command[i-1] != "/":
			j = findEnd(command[i:len(command)])
			f_query = command[i:i+j]
			
		if command[i] == "-" and i+1 != len(command):
			if command[i+1] == "v":
				verbose = 1
			if command[i+1] == "h":
				i += 3
				j = findEnd(command[i:len(command)])
				headers.append(command[i:i+j])
			if command[i+1] == "d":
				i += 3
				type += 1
				if command[i] == "'":
					i += 1
				j = findClose(command[i:len(command)])
				data = delimit(command[i:i+j])
			if command[i+1] == "f":
				i += 3
				type += 2
				j = findEnd(command[i:len(command)])
				input = command[i:i+j]
			if command[i+1] == "o":
				i +=3
				j = findEnd(command[i:len(command)])
				output = command[i:i+j]
			if command[i+1] == "p":
				i +=3
				j = findEnd(command[i:len(command)])
				port = command[i:i+j]
		
		if i+5 < len(command):
			if command[i:i+5] == "http:":
				j = findEnd(command[i:len(command)])
				url = command[i:i+j]
		
		i += 1
		
	request = httpc(status,port,func,verbose,headers,data,input,type,url,output,f_query)
	urlParse(request) 
	return request

def help(func):
	#print(func)
	if func == "get":
		str = """usage: httpc get [-v] [-h key:value] URL\n 
Get executes a HTTP GET request for a given URL.\n\t  
-v \t\t Prints the detail of the response such as protocol, status, and headers.\n\t 
-h key:value \t Associates headers to HTTP Request with the format 'key:value'\n""" 
	elif func == "post":
		str = """usage: httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL\n 
Post executes a HTTP POST request for a given URL with inline data or from file.\n\t 
-v \t\t Prints the detail of the response such as protocol, status, and headers. \n\t 
-h key:value \t Associates headers to HTTP Request with the format 'key:value'.\n\t 
-d string \t Associates an inline data to the body HTTP POST request.\n\t 
-f \t\t file Associates the content of a file to the body HTTP POST request.\n 
Either [-d] or [-f] can be used but not both.\n""" 
	else: 
		str = """httpc is a curl-like application but supports HTTP protocol only.\n 
Usage: \n\t 
httpc command [arguments] \n 
The commands are: \n\t 
get     executes a HTTP GET request and prints the response.\n\t 
post    executes a HTTP POST request and prints the response.\n\t
help    prints this screen. \n 
Use \"httpc help [command]\" for more information about a command.\n""" 
	
	return str
	
def findJSON(output):
	i = 0
	
	if output == "":
		return 0
	while i < len(output):
		if output[i] != "{":
			i += 1
	return i

def httpReq(httpc):
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                 
	s.connect((httpc.host , httpc.port))
	
	header = ' '.join(httpc.headers)
		
	if header != "":
		header = NL + header
	
	if httpc.func == "POST ":
		if httpc.type == 2:
			request = httpc.func +" HTTP/1.0" + NL + "Host: " + httpc.host + header + NL + "Content-Length: " + str(len(httpc.in_data)+len(httpc.ext)) + DL + httpc.ext + NL + httpc.in_data
		else:
			request = httpc.func +" HTTP/1.0" + NL + "Host: " + httpc.host + header + NL + "Content-Length: " + str(len(httpc.data)+len(httpc.ext)) + DL + httpc.ext + NL + httpc.data
	elif httpc.func == "GET ":	
		request = httpc.func + " HTTP/1.0" + NL + "Host: " + httpc.host + header + DL + httpc.ext
	
	request = bytes(request,'utf-8')
	
	s.send(request)
	output = s.recv(4096)
	output = output.decode()
	
	print(output)
	print(httpc.url)
	
	'''if not httpc.verbose:
		i = findJSON(output)
		output = output[i:len(output)]'''
	
	s.close   
	
	return output

def exec(httpc):
	if httpc.status != 1:
		if httpc.status == 0 or httpc.status == 3:
			return print("Error in calling httpc function!")
		if(httpc.status == 2):
			return print(help(httpc.func))
	
	output = ""
	output = httpReq(httpc)
	
	if httpc.output != "":
		o = open(httpc.output, "w")
		o.write(output)
		o.close()
	
	return "\n"+output	
	
while 1:	
	command = input('Enter your httpc request: ') 
	
	if command == "exit":
		break
	
	result = commandParse(command)
	
	#result.prnt()
	
	output = exec(result)

'''
httpc help
httpc help get
httpc help post
httpc post -h Content-Type:application -d '{"Assignment": 1}' http://httpbin.org/post 
httpc post -v -h Content-Type:application/json -d '{"Assignment": 1}' http://httpbin.org/post
httpc post -v -h Content-Type:application/json -f test.txt http://httpbin.org/post
httpc post -v -h Content-Type:application/json -d '{"Assignment": 1}' -f test.txt http://httpbin.org/post -o Out.txt
httpc get 'http://httpbin.org/get?course=networking&assignment=1'
httpc get -v -h abc:1 'http://httpbin.org/get?course=networking&assignment=1'



'''