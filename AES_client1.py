# -*- coding: utf-8 -*-
import socket
from datetime import datetime
from struct import *
import hashlib
import base64 
from Crypto.Cipher import AES
import time


def aes(message,key,iv):
	#secret_key = "Awesome Python!!"
	message64=base64.b64encode(message)#16byte
	if len(message64) % 16 != 0:
		message64_16byte = message64
		for i in range(16-(len(message64) % 16)):
			message64_16byte += "_".encode('utf-8')
	else:
		message64_16byte = message64
	secret_key = hashlib.sha256(key.encode('utf-8')).digest()
	iv = hashlib.md5(iv.encode('utf-8')).digest()
	crypto = AES.new(secret_key,AES.MODE_CBC,iv)
	cipher_data = crypto.encrypt(message64_16byte)
	cipher_data_base64 = base64.b64encode(cipher_data)
	#print(cipher_data)py
	return cipher_data_base64
	#original_message = crypto.decrypt(cipher_data)
	#print(original_message)
	#start = time.time()
def aes_dec(cipher_data_base64,key,iv):
	#secret_key = "Awesome Python!!"
	cipher_data = base64.b64decode(cipher_data_base64)
	secret_key = hashlib.sha256(key.encode('utf-8')).digest()
	iv = hashlib.md5(iv.encode('utf-8')).digest()
	crypto = AES.new(secret_key,AES.MODE_CBC,iv)
	message64_16byte = crypto.decrypt(cipher_data)
	message64 = message64_16byte.split("_".encode('utf-8'))[0]
	message= base64.b64decode(message64)
#	original_message = crypto.decrypt(message)

	return message
	
if __name__ == '__main__':
	iv="hoge"
	secret_key = "Awesome Python!!"
	f=open('./pyramid.jpg', 'rb')
	#f=open('./sao_1.jpg','r')
	data = f.read()
	f.close()
	a=aes(data,secret_key,iv)
	f = open('sao_secret.txt', 'wb') # 書き込みモードで開く
	f.write(a)
	f.close()
	#b=aes_dec(a,secret_key,iv)
	#print(1)
	#f=open("originalfile.jpg","wb")
	#f.write(b)
	#f.close()	
	#address = ('192.168.70.142', 10000)
	#address = ('127.0.0.1', 10000)
	address = ('169.254.17.32', 10000)
	max_size = 4096
	size=500
	print('Starting the client at', datetime.now())
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(address)

	start = time.time()
	end=int(len(a)/size)+1
	all_data=len(a)
	l=pack('H',end)
	client.send(l)
	#m=pack('H',all_data)
	#client.send(m)
	a1=client.recv(max_size)
	#n=pack('H',size)
	#client.send(n)
	print(all_data)
	print(size)
	#for d in range(0,all_data,size):	      
	for d in range(end):
		raw=a[d*size:(d+1)*size]
		client.send(raw)
		r=client.recv(max_size)
		print(unpack('H',r))
		#print(r)
		#start=end
		#end=start+int(len(a)/size)+1
	elapsed_time = time.time() -start
	print("elapsed_time:{0}".format(elapsed_time)+"{sec}")
	print('finish')
	data = client.recv(max_size)
	print('At', datetime.now(), 'someone replied', data)
	client.close()