from packet import Packet
import ipaddress
import time
import socket 
import sys
import os
from math import ceil
from multiprocessing import Process, Event

NL = "\r\n"
DL = "\r\n\r\n"

#=== CLIENT CLASS ========================================================================

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
		print("Host: " + str(self.host))
		print("Port: " + str(self.port))
		print("Ext: " + self.ext)
		print("FQ: " + self.f_query)

#=========================================================================================

#=== PARSING =============================================================================

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
	
	if string[0] == "{":
		while string[i+1] != "}":
			i+=1
				
	elif string[0] == "'":
		i+=1
		while string[i+1] != "'":
			i+=1
		i-=1		
	
	else:
		while i < len(string):
			print(string[i])
			if string[i+1] == " ":
				break
			i += 1
		
	return i+1

	
def urlParse(httpc):
	i = 0
	url = httpc.url
	
	if url == "":
		return 0
	if url[i:i+7] != "http://":
		return 0
		
	i = findSlash(url[7:len(url)])
	httpc.host = ipaddress.ip_address(socket.gethostbyname(url[7:7+i]))
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
			elif command[i+1] == "h":
				i += 3
				j = findEnd(command[i:len(command)])
				headers.append(command[i:i+j])
			elif command[i+1] == "d":
				i += 3
				type += 1
				j = findClose(command[i:len(command)])
				if command[i] == "'":
					i+=1
				data = delimit(command[i:i+j])
			elif command[i+1] == "f":
				i += 3
				type += 2
				j = findEnd(command[i:len(command)])
				input = command[i:i+j]
			elif command[i+1] == "o":
				print(command[i:])
				i +=3
				j = findEnd(command[i:len(command)])
				output = command[i:i+j]
			elif command[i+1] == "p":
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


def findJSON(output):

	i = 0
	
	if output == "":
		return 0
	while i < len(output):
		if output[i] != "{":
			i += 1
	return i


#=========================================================================================

#=== CLIENT FUNCTIONS ====================================================================

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


def httpReq(httpc):
	
	shook = 0
	timeout = 5
	
	#server_ip = ipaddress.ip_address(socket.gethostbyname(httpc.host))
	conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
	try:
	
		header = ' '.join(httpc.headers)
		
		if header != "":
			header = NL + header
	
		if httpc.func == "POST ":
			if httpc.type == 2:
				request = httpc.func +" HTTP/1.0" + NL + "Host: " + str(httpc.host) + header + NL + "Content-Length: " + str(len(httpc.in_data)+len(httpc.ext)) + DL + httpc.ext + NL + httpc.in_data
			else:
				request = httpc.func +" HTTP/1.0" + NL + "Host: " + str(httpc.host) + header + NL + "Content-Length: " + str(len(httpc.data)+len(httpc.ext)) + DL + httpc.ext + NL + httpc.data
		elif httpc.func == "GET ":	
			request = httpc.func + " HTTP/1.0" + NL + "Host: " + str(httpc.host) + header + DL + httpc.ext
	
		#print(request)
		
		hand_shake(conn, httpc)
		
		list = []
		string = ""
		a = 97
		s = 0
		l = 0
		
		while l < 6:
			while s < 1013:
				string += chr(a)
				s+=1
			list.append(string)
			string = ""
			s = 0
			l += 1
			a += 1
		
		list.append(request)
		
		num = len("".join(list).encode('utf-8'))
		
		print(num)
		
		size(conn, httpc, num)
		
		num = int(num / 1013)
		
		select_repeat(conn, httpc, num, list)
		
		output = ""
		output = fin(conn,httpc)
		
		
	except socket.timeout:
		output = 'No response after {}s'.format(timeout)
	finally:
		conn.close()
	
	print(output)
	print(httpc.url)
	
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

#=========================================================================================

#=== UDP =================================================================================

def hand_shake(conn, httpc):
	
	ack = 0
	seq = 0
	
	state = ""
	
	p = Packet()
	
	p.encode("SYN",seq,httpc.host,httpc.port,"")
	
	timeout = 5
	
	while state != "ESTABLISHED":
		try:	
			conn.sendto(p.to_send(), ("localhost", 3000))
			conn.settimeout(timeout)
				
			response, sender = conn.recvfrom(1024)
			
			p.decode(response)
			p.prnt()
			
			if p.PacketType == "SYN-ACK":
		
				ack = p.SequenceNumber + 1
				seq = int(p.Payload) + 1
		
				p.encode("ACK",seq,httpc.host,httpc.port,str(ack))
		
				conn.sendto(p.to_send(),("localhost", 3000))
			
				state = "ESTABLISHED"
				print(state + "\n")
			
		except socket.timeout:
			print("Timeout Expired: " + str(timeout) + "s\n")


def size(conn,httpc,num):
	
	timeout = 5
	
	try:
		p = Packet()
		p.encode("Data",0,httpc.host,httpc.port,str(num))
		conn.sendto(p.to_send(),("localhost", 3000))
		conn.settimeout(timeout)
		
		response, sender = conn.recvfrom(1024)
		p.decode(response)
		p.prnt()
		
		print("Size Delivered\n")
		
	except socket.timeout:
		print("Timeout Expired: " + str(timeout) + "s\n")
	

def select_repeat(conn,httpc,num,snd_array):
	
	i = 0
	ack = 0
	seq = 0
	num = len(snd_array)
	window_base = 0
	window_width = int(num / 2)
	window_edge = window_width
	
	ack_buffer = [-1]
	
	timeout = 5
	
	print(num)
	
	print(snd_array)
	
	while window_base < num:
		
		while i < window_edge:
			
			try:
				p = Packet()
				
				if i != 1:
					p.encode("Data",i,httpc.host,httpc.port,snd_array[i])
				
					conn.sendto(p.to_send(),("localhost", 3000))
				
					conn.settimeout(timeout)
				
				i+=1
			
			except socket.timeout:
				print("Timeout Expired: " + str(timeout) + "s\n")
		
		try:
			response, sender = conn.recvfrom(1024)
			p.decode(response)
			p.prnt()
		
			ack = int(p.Payload)
		
			if ack_buffer[0] == -1:
				ack_buffer.pop(0)
			ack_buffer.append(ack)
			ack_buffer.sort()
			
					
		except socket.timeout:
			print("Timeout Expired: " + str(timeout) + "s\n")
			
			
			if window_base not in ack_buffer:
				j = window_base 
				p.encode("Data",j,httpc.host,httpc.port,snd_array[j])
				conn.sendto(p.to_send(),("localhost", 3000))
				
				conn.settimeout(timeout)
		
		while window_base == ack_buffer[0]:
			
			if window_base == ack_buffer[0]:
				
				if len(ack_buffer) == 1:
					ack_buffer.pop(0)
					ack_buffer.append(-1)
				else:
					ack_buffer.pop(0)
				window_base += 1
				window_edge = window_base + window_width
				
				if window_edge > num:
					window_edge = num
				
				
def fin(conn,httpc):
	
	ack = 0
	seq = 0
	
	terminate = 0
	status = ""
	output = ""
	
	timeout = 5
	
		
	while status != "PENDING":
	
		try:
			p = Packet()
			p.encode("FIN",seq,httpc.host,httpc.port,"")
			
			conn.sendto(p.to_send(),("localhost", 3000))	
			conn.settimeout(timeout)
		
			response, sender = conn.recvfrom(1024)
			p.decode(response)
			p.prnt()
			
			if p.PacketType == "Data":
				output = p.Payload
				print("Received final file from server")
				
				response, sender = conn.recvfrom(1024)
				p.decode(response)
				p.prnt()
				
			if p.PacketType == "ACK":
				status = "PENDING"
				print(status + "\n")
				
		except socket.timeout:
			print("Timeout Expired: " + str(timeout) + "s\n")
		
	
	while status != "TERMINATED":
	
		try:
			p = Packet()
			response, sender = conn.recvfrom(1024)
			p.decode(response)
			p.prnt()
			
			if p.PacketType == "FIN":
				p.encode("ACK",seq,httpc.host,httpc.port,str(0))
				
				status = "TERMINATED"
				print(status + "\n")
				conn.sendto(p.to_send(),("localhost", 3000))	
				conn.settimeout(timeout)
				
				
			
		except socket.timeout:
			print("Timeout Expired: " + str(timeout) + "s\n")
			break
	return output
	
				
#=========================================================================================

#===== MULTI =============================================================================

def task(event,result):
	proc_id = os.getpid()
	event.wait()
	print('timestamp of process id {}: {}'.format(proc_id, time.time()))
	return exec(result)

#=========================================================================================

#===== PROGRAM ===========================================================================	


while 1:	
	
	command = input('Enter your httpc request: ') 
	
	if command == "exit":
		break
	
	result = commandParse(command)
	
	result.prnt()
	
	'''event = Event()
	
	p1 = Process(target=task,args=(event,result))
	#p2 = Process(target=task,args=(event,result))
	
	p1.start()
	#p2.start()
	
	event.set()'''
	
	output = exec(result)


#===== END ===============================================================================





'''
httpc post -d Yhohosfhaslk -p 8080 http://localhost/Test543
httpc get -p 8080 http://localhost/Test543.txt









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