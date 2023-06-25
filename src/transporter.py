#!/usr/bin/env python3

import sys
import os
import netifaces
import socket
import codecs

# -------------------------- INFO --------------------------

def basic():
	global proceed
	proceed = False
	print("Transporter v2.5 ( github.com/ivan-sincek/transporter )")
	print("")
	print("Usage:   python3 transporter.py -i interface -p protocol -f file       [-o out         ]")
	print("Example: python3 transporter.py -i eth0      -p 0        -f packet.txt [-o response.txt]")

def advanced():
	basic()
	print("")
	print("DESCRIPTION")
	print("    Send packets through raw sockets")
	print("INTERFACE")
	print("    Network interface to use")
	print("    -i <interface> - eth0 | wlan0 | etc.")
	print("PROTOCOL")
	print("    Network protocol to use")
	print("    Use '0' for ICMP")
	print("    Use '6' for TCP")
	print("    Use '7' for UDP")
	print("    Search web for additional network protocol numbers")
	print("    -p <protocol> - 0 | 6 | 17 | etc.")
	print("FILE")
	print("    File with the packet to send")
	print("    -f <file> - packet.txt | etc.")
	print("OUT")
	print("    Output file")
	print("    -o <out> - response.txt | etc.")

# -------------------- VALIDATION BEGIN --------------------

# my own validation algorithm

proceed = True

def print_error(msg):
	print(("ERROR: {0}").format(msg))

def error(msg, help = False):
	global proceed
	proceed = False
	print_error(msg)
	if help:
		print("Use -h for basic and --help for advanced info")

args = {"interface": None, "protocol": None, "file": None, "out": None}

def validate(key, value):
	global args
	value = value.strip()
	if len(value) > 0:
		if key == "-i" and args["interface"] is None:
			args["interface"] = value
			try:
				netifaces.ifaddresses(args["interface"])[netifaces.AF_LINK][0]["addr"]
			except ValueError:
				error("Interface name is not valid")
		elif key == "-p" and args["protocol"] is None:
			args["protocol"] = value
			if not args["protocol"].isdigit():
				error("Protocol must be numeric")
			else:
				args["protocol"] = int(args["protocol"])
		elif key == "-f" and args["file"] is None:
			args["file"] = value
			if not os.path.isfile(args["file"]):
				error("File does not exists")
			elif not os.access(args["file"], os.R_OK):
				error("File does not have read permission")
			elif not os.stat(args["file"]).st_size > 0:
				error("File is empty")
		elif key == "-o" and args["out"] is None:
			args["out"] = value

def check(argc, args):
	count = 0
	for key in args:
		if args[key] is not None:
			count += 1
	return argc - count == argc / 2

argc = len(sys.argv) - 1

if argc == 0:
	advanced()
elif argc == 1:
	if sys.argv[1] == "-h":
		basic()
	elif sys.argv[1] == "--help":
		advanced()
	else:
		error("Incorrect usage", True)
elif argc % 2 == 0 and argc <= len(args) * 2:
	for i in range(1, argc, 2):
		validate(sys.argv[i], sys.argv[i + 1])
	if args["interface"] is None or args["protocol"] is None or args["file"] is None or not check(argc, args):
		error("Missing a mandatory option (-i, -p, -f) and/or optional (-o)", True)
else:
	error("Incorrect usage", True)

# --------------------- VALIDATION END ---------------------

# ----------------------- TASK BEGIN -----------------------

def write_file(data, out):
	confirm = "yes"
	if os.path.isfile(out):
		print(("'{0}' already exists").format(out))
		confirm = input("Overwrite the output file (yes): ")
	if confirm.lower() == "yes":
		open(out, "w").write(data)
		print(("Response has been saved to '{0}'").format(out))

def send(interface, protocol, packet, out = None):
	error = False
	soc = None
	try:
		soc = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
		soc.settimeout(1)
		soc.bind((interface, protocol))
		try:
			print("Sending the packet...")
			soc.send(packet)
			print("Packet has been sent successfully")
		except socket.timeout:
			error = True
			print("Sending the packet timed out")
		if not error:
			print("")
			response = ""
			try:
				print("Waiting for the response...")
				while True:
					read = soc.recv(1024)
					if not read:
						break
					response += read.decode("unicode_escape")
			except socket.timeout:
				print("Waiting for the response timed out")
			if not response:
				print("No response has been received or is empty")
			elif out:
				write_file(response, out)
			else:
				print("---------- RESPONSE START ----------")
				print(response)
				print("----------- RESPONSE END -----------")
	except OverflowError:
		print_error("Protocol is not valid")
	except socket.error as ex:
		print_error(ex)
	finally:
		if soc:
			soc.close()

if proceed:
	print("############################################################")
	print("#                                                          #")
	print("#                     Transporter v2.5                     #")
	print("#                            by Ivan Sincek                #")
	print("#                                                          #")
	print("# Send packets through raw sockets.                        #")
	print("# GitHub repository at github.com/ivan-sincek/transporter. #")
	print("#                                                          #")
	print("############################################################")
	packet = open(args["file"], "rb").read()
	packet = (b"").join(packet.split())
	packet = codecs.encode(packet.decode("unicode_escape"), "raw_unicode_escape")
	send(args["interface"], args["protocol"], packet, args["out"])

# ------------------------ TASK END ------------------------
