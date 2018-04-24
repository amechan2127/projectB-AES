from Crypto.Cipher import AES
import time


def aes(message):
	secret_key = "Awesome Python!!"
	crypto = AES.new(secret_key)
	cipher_data = crypto.encrypt(message)
	#print(cipher_data)
	return cipher_data
	#original_message = crypto.decrypt(cipher_data)
	#print(original_message)
if __name__ == '__main__':
	message = "This is enc Test"
	for i in range(10):
		start = time.time()	
		a=aes(message)
		elapsed_tme = time.time() - start
		print(elapsed_tme)



