from twilio.rest import Client
import os
import sys

notify_secret = "notify_secret.txt"
path = os.path.join(sys.path[0], notify_secret)
print(path)
f = open(path)
lines = f.readlines()
setting_0 = lines[0].strip()
setting_1 = lines[1].strip()
setting_2 = lines[2].strip()
setting_3 = lines[3].strip()
setting_4 = lines[4].strip()

account_sid = setting_0
auth_token = setting_1

client = Client(account_sid, auth_token)

to_phone = setting_2
service_phone = setting_3
debug_phone = setting_4

def sendText(msg="NA"):
	# message = client.messages.create(
	# 	to=to_phone,
	# 	from_=service_phone,
	# 	body=msg)
	
	message = client.messages.create(
		to=debug_phone,
		from_=service_phone,
		body=msg)
	
	print(message.sid)

