from math import floor, sqrt
from random import uniform
import ipaddress

def typeEncode(string):
		
		byte = -1
		
		if string == "Data":
			byte = 0
		elif string == "ACK":
			byte = 1
		elif string == "SYN":
			byte = 2
		elif string == "SYN-ACK":
			byte = 3
		elif string == "NACK":
			byte = 4
		elif string == "FIN":
			byte = 5
		
		byte = byte.to_bytes(1, byteorder='big')
		
		return byte

def seqEncode(string):
	
	num = int(string)
	
	byte = num.to_bytes(4, byteorder='big')
	
	return byte
	
def addrEncode(string):
	
	addr = ipaddress.ip_address(string)
	
	byte = addr.packed
	
	return byte

def portEncode(string):
	
	num = int(string)
	
	byte = num.to_bytes(2, byteorder='big')
	
	return byte


def typeDecode(byte):
		
		string = ""
		
		num = int.from_bytes(byte, byteorder='big')
		
		if num == 0:
			string = "Data"
		elif num == 1:
			string = "ACK"
		elif num == 2:
			string = "SYN"
		elif num == 3:
			string = "SYN-ACK"
		elif num == 4:
			string = "NACK"
		elif num == 5:
			string = "FIN"
		
		return string

def seqDecode(byte):
	
	num = int.from_bytes(byte, byteorder='big')
	
	return num
	
def addrDecode(byte):
	
	string = str(byte[0]) + "." + str(byte[1]) + "." + str(byte[2]) + "." + str(byte[3])
	addr = ipaddress.ip_address(string)
	
	return addr

def portDecode(byte):
	
	num = int.from_bytes(byte, byteorder='big')
	
	return num
	
	
class Packet:
			
	def __init__(self):
		self.PacketTypeE = ""
		self.SequenceNumberE = -1
		self.PeerAddressE = ipaddress.ip_address("127.0.0.1")
		self.PeerPortNumberE = -1
		self.PayloadE = ""
		self.size = -1
		
		self.PacketType = ""
		self.SequenceNumber = -1
		self.PeerAdress = ipaddress.ip_address("127.0.0.1")
		self.PeerPortNumber = -1
		self.Payload = ""
	
	def encode_server(self):
		
		self.PacketTypeE = typeEncode(self.PacketType)
		self.SequenceNumberE = seqEncode(self.SequenceNumber)
		self.PeerAddressE = addrEncode(self.PeerAddress)
		self.PeerPortNumberE = portEncode(self.PeerPortNumber)
		self.PayloadE = self.Payload.encode("utf-8")
		
	def encode(self, PacketType,SequenceNumber,PeerAddress,PeerPortNumber,Payload):
		
		self.PacketTypeE = typeEncode(PacketType)
		self.SequenceNumberE = seqEncode(SequenceNumber)
		self.PeerAddressE = addrEncode(PeerAddress)
		self.PeerPortNumberE = portEncode(PeerPortNumber)
		self.PayloadE = Payload.encode("utf-8")
		self.size = len(self.PayloadE)
	
	def decode(self,buf):
		
		self.PacketType = typeDecode(buf[0:1])
		self.SequenceNumber = seqDecode(buf[1:5])
		self.PeerAddress = addrDecode(buf[5:9])
		self.PeerPortNumber = portDecode(buf[9:11])
		self.Payload = buf[11:].decode("utf-8")
	
	def to_send(self):
		buf = bytearray()
		buf.extend(self.PacketTypeE)
		buf.extend(self.SequenceNumberE)
		buf.extend(self.PeerAddressE)
		buf.extend(self.PeerPortNumberE)
		buf.extend(self.PayloadE)
		
		return buf
	
	def output(self):
		string = "PackeType: " + self.PacketType + "\nSequenceNumber: " + str(self.SequenceNumber) + "\nPeerAddress: " + str(self.PeerAddress) + "\nPeerPortNumber: " + str(self.PeerPortNumber) + "\nPayload: " + self.Payload
		return string
		
	def prnt(self):
		
		print("PackeType: " + self.PacketType)
		print("SequenceNumber: " + str(self.SequenceNumber))
		print("PeerAddress: " + str(self.PeerAddress))
		print("PeerPortNumber: " + str(self.PeerPortNumber))
		print("Payload: " + self.Payload)
		print()
		
def initSeq():
	
	return floor(uniform(0,4294967295))


'''yo = Packet()

yo.encode("Data",100000,"127.0.0.1",8007,"hello")

yo.decode(yo.to_send())

yo.prnt()


byte = bytes("127","utf-8")
print(str(int(byte)))'''






















