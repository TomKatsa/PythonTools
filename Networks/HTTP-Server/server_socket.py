import socket
import os

IP = "0.0.0.0"
PORT = 8000
SERV_DIR = "C:\wwwproject"

os.chdir(SERV_DIR)



#Makes a header for the HTTP response
def make_header(state, data):
    if state == "ok":
        print("Data after header: ")
        print(data)
        header = "HTTP/1.1 200 OK\r\n"
        header += "Content-Length: " + str(len(data)) + "\r\n\r\n"
    elif state == "nf":
        header = "HTTP/1.1 404 Not Found\r\n\r\n\r\n"

    else:
        header = "HTTP/1.1 999 Unimplemented"
    print("Header: ")
    print(header)
    return header


#Reads file. Returns if file was found (ok) 200 or not (nf) 404
def read_file(file):
    try:
        with open(file, "r", encoding="UTF-8") as f:
            print("File found, returning data.")
            return f.read(), "ok"
    except FileNotFoundError:
        print("Resource was not found.")
        return "File Not Found", "nf"


#Parsing the request
def parse_request(resource):
    if resource == "/":
        data, state = read_file("index.html")
        print("Returning index file.")
        return make_header(state, data) + data
    data, state = read_file(resource[1:])
    return make_header(state, data) + data


#Making sure the request is valid before parsing the resource.
def validate_request(request):
    print(request)
    first_line = request.splitlines()[0]
    first_line = first_line.split(' ')
    req, resource, ver = first_line[0], first_line[1], first_line[2]
    if req == "GET" and ver == "HTTP/1.1":
        return True, resource
    else:
        return False, 0


#Main function - validating the request, parsing and sending back headers and content.
def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    valid, resource = validate_request(request)
    if valid:
        print("Valid request.")
        data = parse_request(resource)
        client_socket.send(data.encode())
    else:
        print("Invalid request.")
        client_socket.close()


def main_loop():
    print("--------------------------------------------------------")
    print("Server address: ")
    print(socket.gethostbyname_ex(socket.gethostname())[2][1])
    print("Port: ")
    print(PORT)
    print("--------------------------------------------------------")
    server_socket = socket.socket()
    server_socket.bind((IP, PORT))
    server_socket.listen(10)
    while True:
        (client_socket, client_address) = server_socket.accept()
        print("Connected to a client")
        handle_client(client_socket)


main_loop()
