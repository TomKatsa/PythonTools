import socket
import threading

IP = "192.168.14.79"
PORT = 8182


def threaded_response(me):
	while True:
		response = me.recv(1024)
		print(response.decode())



if __name__ == "__main__":
	me = socket.socket()
	me.connect((IP, PORT))
	x = threading.Thread(target=threaded_response, args=(me,))
	x.start()
	while True:
		msg = input("")
		me.send(msg.encode())