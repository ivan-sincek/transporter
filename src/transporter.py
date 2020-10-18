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
	print("Transporter v1.0 ( github.com/ivan-sincek/transporter )")
	print("")
	print("Usage:   python3 transporter.py -i interface -p protocol -f file")
	print("Example: python3 transporter.py -i eth0      -p 0        -f packet.txt")

def advanced():
	basic()
	print("")
	print("DESCRIPTION")
	print("    Send packets through raw sockets")
	print("INTERFACE (required)")
	print("    Specify a network interface to use")
	print("    -i <interface> - eth0 | wlan0 | etc.")
	print("PROTOCOL (required)")
	print("    Specify a network protocol to use")
	print("    Use '0' for ICMP")
	print("    Use '6' for TCP")
	print("    Use '7' for UDP")
	print("    Search web for additional network protocol numbers")
	print("    -p <protocol> - 0 | 6 | 17 | etc.")
	print("FILE (required)")
	print("    Specify a file with the packet you want to send")
	print("    -f <file> - packet.txt | etc.")

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

args = {"interface": None, "protocol": None, "file": None}

def validate(key, value):
	global args
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
		elif not os.stat(args["file"]).st_size > 0:
			error("File is empty")

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
elif argc % 2 == 0 and argc <= 6:
	for i in range(1, argc, 2):
		validate(sys.argv[i], sys.argv[i + 1])
	if args["interface"] == None or args["protocol"] == None or args["file"] == None or not check(argc, args):
		error("Missing a mandatory option (-i, -p, -f)", True)
else:
	error("Incorrect usage", True)

# --------------------- VALIDATION END ---------------------

# ----------------------- TASK BEGIN -----------------------

def send(interface, protocol, file):
	soc = None
	try:
		soc = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
		soc.settimeout(1)
		soc.bind((interface, protocol))
		packet = open(file, "rb").read()
		packet = (b"").join(packet.split())
		packet = codecs.encode(packet.decode("unicode_escape"), "raw_unicode_escape")
		print("Sending the packet...")
		soc.send(packet)
		print("Packet was sent successfully")
		print("")
		print("Waiting for a response...")
		response = ""
		while True:
			read = soc.recv(1024)
			if not read:
				break
			response += read.decode("unicode_escape")
		if len(response) > 0:
			open("transporter_response.txt", "w").write(response)
			print("Response has been saved to 'transporter_response.txt'")
		else:
			print("Response is empty")
	except OverflowError:
		print_error("Protocol number is not valid")
	except socket.timeout:
		print("Timed out")
	except socket.error as ex:
		print_error(ex)
	finally:
		if soc is not None:
			soc.close()

if proceed:
	print("######################################################################")
	print("#                                                                    #")
	print("#                          Transporter v1.0                          #")
	print("#                                 by Ivan Sincek                     #")
	print("#                                                                    #")
	print("# Send packets through raw sockets.                                  #")
	print("# GitHub repository at github.com/ivan-sincek/transporter.           #")
	print("# Feel free to donate bitcoin at 1BrZM6T7G9RN8vbabnfXu4M6Lpgztq6Y14. #")
	print("#                                                                    #")
	print("######################################################################")
	send(args["interface"], args["protocol"], args["file"])

# ------------------------ TASK END ------------------------
