import os
import subprocess
import socket
import multiprocessing
import sys

def craft_subnet(gateway):
	chunks = gateway.split('.')
	subnet = []
	for i in range(3): # Subnet mask: 255.255.255.0 (x.x.x.x/24)
		subnet.append(chunks[i])
	return subnet

def ping(ip):
	ping = ["ping", "-n", "1", "-w", "1", ip]
	host_up = subprocess.call(ping, shell=True, stdout=open(os.devnull, "w"))==0 # If the call returns 0, the host is up.
	return ip if host_up else 0

def ip_list(subnet):
	il = []
	for i in range(256):
		il.append('.'.join(subnet) + "." + str(i))
	return il # Generates all the IPs to scan using the subnet





def sweep(subnet):
	hosts = []
	str_sub = '.'.join(subnet)
	for i in range(256):
		ip = str_sub + "." + str(i)
		print(f"Pinging IP: {ip}")
		response = ping(ip)
		if response:
			print("Host is up!")
			hosts.append(ip)
		else:
			print("Host is down.")
	return hosts



def main():
	if len(sys.argv) == 2:
		gate = sys.argv[1]
	else:
		gate = input("[*] Enter gateway address:")
	subnet = craft_subnet(gate)
	print(f"[*] Pinging 256 addresses on {gate}/24 subnet...")
	iplist = ip_list(subnet)
	p = multiprocessing.Pool(16)
	pinglist = p.map(ping, iplist)
	#NUL = open(os.devnull, 'w')
	#print(list(pinglist))
	#print(list(map(ping, s)))
	#up_hosts = check_hosts(iplist, pinglist)
	up_hosts = [x for x in pinglist if x!=0]
	#print(up_hosts)
	for ip in up_hosts:
		try:
			ns = socket.gethostbyaddr(ip)[0]
		except:
			ns = "Unknown Host"
		print(f"[+] {ip} is up. // {ns} //")
	print("[*] Done!")
	input()


# subnet = craft_subnet(input("Enter default gateway IP:"))
# print(subnet)
# hosts = sweep(subnet)
# for host in hosts:
# 	print("{} is up. [{}]".format(host, socket.gethostbyaddr(host)))
# print("Total: {} hosts up.".format(len(hosts)))
# input()

if __name__ == '__main__' :
	main()


