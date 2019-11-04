import threading
import socket

IP = "0.0.0.0"
PORT = 8182
clients = {}
# count = 1
# def count():
# 	start = 1
# 	while start<100:
# 		yield start
# 		start += 1

# counter = count()

def serve(client, num):

	name = f"Client{num}"
	#count += 1
	clients[name] = client
	ip = client.getsockname()[0]
	print(f"{name} has joined the server, from address {ip}")
	client.send(f"Welcome to the chat room, {name}!\n----------------------------".encode())
	msg = "1"
	while msg:
		try:
			msg = client.recv(1024)
			broadcast(msg, name)
		except:
			break
	print(f"{name} dropped connection.")
	clients.pop(name)


def broadcast(msg, name):
	for c in clients:
		cmsg = "[{}]: {}".format(name, msg.decode())
		clients[c].send(cmsg.encode())


if __name__ == "__main__":
	server = socket.socket()
	server.bind((IP, PORT))
	server.listen(5)
	num = 1
	while True:
		client, address = server.accept()
		x = threading.Thread(target=serve, args=(client,num))
		num += 1
		x.start()

