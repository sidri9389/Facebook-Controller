#https://github.com/carpedm20/fbchat

import fbchat
import time


email = "tdrvlad@gmail.com"
password = "12345678901234567890"

command_password = "please"

log_file = "Log.txt"

session = fbchat.Session.login(email, password)
listener = fbchat.Listener(session=session, chat_on=False, foreground=False)

verified_users = []

commands = {"Porneste" : 1, "Opreste" : 0, "Verifica" : 2}
devices = {""}


for event in listener.listen():
	if isinstance(event, fbchat.MessageEvent):
		
		if event.author.id != session.user.id:
			
			thread = event.thread

			if event.author not in verified_users:

				thread.send_text("Hello")
				time.sleep(1.5)
				thread.send_text("Type Password")

				time.sleep(7)

				responses = thread.fetch_messages(limit = 1)

				for response in responses:

					print(response.text)
					if command_password == response.text:
							thread.send_text("Access Granted")
							verified_users.append(event.author)

							f = open(log_file,"w")
							f.write("Added user " + str(event.author.id))
							f.close()
					else:
							thread.send_text("Acces Denied")

			else:

				message = event.message.text
				
				thread.send_text(message)
				print(message)
				#thread.send_text("Welcome, how can I help?")
				#time.sleep(1.5)



			







