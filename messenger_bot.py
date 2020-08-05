#https://www.thepythoncode.com/article/make-bot-fbchat-python
#https://github.com/carpedm20/fbchat/tree/master/examples

##>>
#https://fbchat.readthedocs.io/en/stable/
import fbchat
from fbchat import log, Client
from fbchat.models import Message, MessageReaction

# facebook user credentials
username = "tdrvlad@gmail.com"
password = "12345678901234567890"

# Subclass fbchat.Client and override required methods
'''
class EchoBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)

        log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))

        # If you're not the author, echo
        if author_id != self.uid:
            self.send(message_object, thread_id=thread_id, thread_type=thread_type)


client = EchoBot(username, password)
client.listen()

'''
# login
client = Client(username, password)

# get 20 users you most recently talked to
users = client.fetchThreadList()
print(users)

# get the detailed informations about these users
detailed_users = [ list(client.fetchThreadInfo(user.uid).values())[0] for user in users ]

# sort by number of messages
sorted_detailed_users = sorted(detailed_users, key=lambda u: u.message_count, reverse=True)

# print the best friend!
best_friend = sorted_detailed_users[0]

print("Best friend:", best_friend.name, "with a message count of", best_friend.message_count)

# message the best friend!
'''
'''
client.send(Message(
                    text=f"Congratulations {best_friend.name}, you are my best friend with {best_friend.message_count} messages!"
                    ),
            thread_id=best_friend.uid)
'''
'''
# get all users you talked to in messenger in your account
all_users = client.fetchAllUsers()

print("You talked with a total of", len(all_users), "users!")

# let's logout
client.logout()


session = fbchat.Session.login(username, password)
listener = fbchat.Listener(session=session, chat_on=False, foreground=False)

for event in listener.listen():
    if isinstance(event, fbchat.MessageEvent):
        print(f"{event.message.text} from {event.author.id} in {event.thread.id}")
        # If you're not the author, echo
        if event.author.id != session.user.id:
            event.thread.send_text(event.message.text)
