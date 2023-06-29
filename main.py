from models import Quote
from connect import Atlas_Server
from seeds import authors
from mongoengine.queryset.visitor import Q
"""
create connection with Atlas DB
"""
server = Atlas_Server("config.ini")
server.connect()

NAME_CMD = "name"
TAG_CMD = "tag"
TAGS_CMD = "tags"
FS = ","  ## field separator in the argument list
CS = ":"  ## separator between command and argument list
"""
use handles to evaluate the commands
for the tags command two words splitted by , are required only
"""

commands = [NAME_CMD, TAGS_CMD, TAG_CMD]
handler = {
    NAME_CMD:
    lambda name: Quote.objects(author=authors[name]),
    TAG_CMD:
    lambda tag_name: Quote.objects(tags=tag_name),
    TAGS_CMD:
    lambda tag_list: Quote.objects(
        Q(tags=tag_list.split(FS)[0]) | Q(tags=tag_list.split(FS)[1]))
}

command = ""
while True:
    line = input(">> ")
    ######line = "exit"
    try:
        command, args = line.split(CS)
        if command in commands:
            try:
                list = handler[command](args)
                for element in list:
                    print(element.quote.encode())
            ####print(args)
            except:
                print(">> can not execute. Please check arguments.")

    except ValueError:
        command = line
        if command == "exit":
            break

        print(">> do not understand the command. Must be name:args or exit")
