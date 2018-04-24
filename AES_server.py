from Crypto.Cipher import AES
from datetime import datetime
import socket
from struct import *
import os
import base64
import hashlib


if os.path.isfile('text.jpg'):
    os.remove('text.jpg')

address = ('127.0.0.1', 10000)
max_size = 1024*5

def aes_dec(cipher_data_base64,key,iv):
	cipher_data = base64.b64decode(cipher_data_base64)
	secret_key = hashlib.sha256(key.encode('utf-8')).digest()
	iv = hashlib.md5(iv.encode('utf-8')).digest()
	crypto = AES.new(secret_key,AES.MODE_CBC,iv)
	message64_16byte = crypto.decrypt(cipher_data)
	message64 = message64_16byte.split("_".encode('utf-8'))[0]
	message= base64.b64decode(message64)
	return message

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

	f = open('text.jpg', 'ab') # 書き込みモードで開く

	for i in range(allsize[0]):
		data = client.recv(max_size)
		j = pack('H',i)
		print(i)
		f.write(data) # 引数の文字列をファイルに書き込む
		client.send(j)
   
	f.close() # ファイルを閉じる
	secret_key='Awesome Python!!'
	iv='hoge'
	f = open('text.jpg','rb')
	a = f.read()
	f.close()
	
	b=aes_dec(a,secret_key,iv)
	print(b)
	f=open("originalfile.jpg","wb")
	f.write(b)
	f.close()
	client.sendall(b"Finish")
	client.close()
	server.close()