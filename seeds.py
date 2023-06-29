from models import Author, Quote, Authors
import json
from connect import Atlas_Server
""" 
create connection with Atlas
"""

server = Atlas_Server("config.ini")
server.connect()
"""
read json files and create upload to database for Authors
"""
with open("authors.json", "r") as fh:
    list = json.load(fh)
"""
create class to accumulate authors references
"""
authors = Authors()

for element in list:
    fullname1 = element["fullname"]
    born_date1 = element["born_date"]
    born_location1 = element["born_location"]
    description1 = element["description"]

    author = Author(fullname=fullname1,
                    born_date=born_date1,
                    born_location=born_location1,
                    description=description1)

    authors.append(author)
    author.save()
"""
read json files and create upload to database for Quotes
"""
with open("quotes.json", "r") as fh:
    list = json.load(fh)

for element in list:
    tags1 = element["tags"]
    quote1 = element["quote"]
    author1 = authors[element["author"]]
    quote = Quote(tags=tags1, author=author1, quote=quote1)
    quote.save()
