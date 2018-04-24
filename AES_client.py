import socket
from datetime import datetime
from struct import *
import hashlib
import base64 
from Crypto.Cipher import AES
import time

address = ('169.254.17.32', 10000)
#address = ('127.0.0.1', 10000)
max_size = 4096
size=500

def aes_enc(message,key,iv):
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
	return cipher_data_base64

if __name__ == '__main__':
	print('Starting the client at', datetime.now())
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(address)
	start = time.time()
	iv="hoge"
	secret_key = "Awesome Python!!"
	f=open('./earth.jpg', 'rb')
	data = f.read()
	f.close()
	a=aes_enc(data,secret_key,iv)
	f = open('sao_secret.txt', 'wb') # 書き込みモードで開く
	f.write(a)
	f.close()

	end=int(len(a)/size)+1
	all_data=len(a)
	l=pack('H',end)
	client.send(l)
	a1=client.recv(max_size)
	print(all_data)
	print(size)      
	for d in range(end):
		enc=a[d*size:(d+1)*size]
		client.send(enc)
		r=client.recv(max_size)
		print(unpack('H',r))
	elapsed_time = time.time() -start
	print("elapsed_time:{0}".format(elapsed_time)+"{sec}")
	print('finish')
	data = client.recv(max_size)
	print('At', datetime.now(), 'someone replied', data)
	client.close()