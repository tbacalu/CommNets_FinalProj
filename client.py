import requests
import sys
import json

def getMessages(user):
	params = {"user":user}
	r = requests.get("http://ec2-3-143-68-118.us-east-2.compute.amazonaws.com", params)
	print(f"\nMessages for {user}:")
	for message in r.json()['messages']:
		print(f"({message['sender']}) {message['value']}")
	print("")

def send(to_usr, msg):
	print(f"Sending {msg} to {to_user}")
	data = {"sender": user, "receiver": to_user, "message": msg}
	r = requests.post("http://ec2-3-143-68-118.us-east-2.compute.amazonaws.com", data)

user = sys.argv[1]
getMessages(user)

while True:
	print("Choose a command:\n1) refresh\n2) send:<to_usr>:<msg>\n3) quit")
	resp = input()

	if resp[:4].lower() == "send":
		resp = resp.split(':')
		send(resp[1], resp[2])

	elif resp.lower() == "refresh":
		getMessages(user)
	
	elif resp.lower() == "quit":
		break
