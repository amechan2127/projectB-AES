from Crypto.Cipher import AES
from datetime import datetime
import socket
from struct import *
#address = ('192.168.70.142', 10000)
address = ('127.0.0.1', 10000)
max_size = 1024*5
import os
import base64
import hashlib


if os.path.isfile('text.jpg'):
    os.remove('text.jpg')

def aes_dec(cipher_data_base64,key,iv):
	#secret_key = "Awesome Python!!"
	cipher_data = base64.b64decode(cipher_data_base64)
	#print(cipher_data)
	secret_key = hashlib.sha256(key.encode('utf-8')).digest()
	#print(secret_key)
	iv = hashlib.md5(iv.encode('utf-8')).digest()
	#print(iv)
	crypto = AES.new(secret_key,AES.MODE_CBC,iv)
	#print(crypto)
	message64_16byte = crypto.decrypt(cipher_data)
	message64 = message64_16byte.split("_".encode('utf-8'))[0]
	message= base64.b64decode(message64)
	return message
#	original_message = crypto.decrypt(message)

if __name__ == '__main__':
	print('Starting the server at', datetime.now())
	print('Waiting for a client to call.')
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(address)
	server.listen(5)

	client, addr = server.accept()
 
	num = client.recv(max_size)
	client.send(num)
 
	allsize=unpack('H',num)
	print(allsize) 
	#num1 = client.recv(max_size)
	#client.send(num1)
	#size=unpack('H',num1) 
	#print(size)
 	
	#while data[-6:-1] != b'finish':
	#for i in range(n[0]+2):
	#f = open('text.txt', 'wab') # 書き込みモードで開く
	f = open('text.jpg', 'ab') # 書き込みモードで開く
	#for i in range(0,allsize[0],size[0]):
	for i in range(allsize[0]):
		data = client.recv(max_size)
		#data_receive.append(data)
		j = pack('H',i)
		print(i)
		f.write(data) # 引数の文字列をファイルに書き込む
		client.send(j)

	#print('At', datetime.now(), client, 'said',data)    
	f.close() # ファイルを閉じる
	secret_key='Awesome Python!!'
	iv='hoge'
	f = open('text.jpg','rb')
	a = f.read()
	f.close()
	#print(a)
	
	b=aes_dec(a,secret_key,iv)
	print(b)
	f=open("originalfile.jpg","wb")
	f.write(b)
	f.close()
	client.sendall(b"Finish")
	client.close()
	server.close()