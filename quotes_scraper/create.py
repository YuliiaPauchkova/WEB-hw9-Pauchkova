from mongoengine import Document, StringField, ListField, ReferenceField, connect
import json

connect(
    db='database',
    host='mongodb+srv://new1:2312@database.9kdee0f.mongodb.net/',
)

class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, required=True)
    quote = StringField()

def save_authors(authors_data):
    for author_data in authors_data:
        author = Author(
            fullname=author_data['fullname'],
            born_date=author_data.get('born_date', ''),
            born_location=author_data.get('born_location', ''),
            description=author_data.get('description', '')
        )
        author.save()

def save_quotes(quotes_data, authors_dict):
    for quote_data in quotes_data:
        author_name = quote_data['author']
        author_info = authors_dict.get(author_name)
        if author_info:
            author = Author.objects(fullname=author_name).first()
            if not author:
                author = Author(**author_info)
                author.save()
            quote = Quote(
                tags=quote_data['tags'],
                author=author, 
                quote=quote_data['quote']
            )
            quote.save()

with open('authors.json', 'r') as f:
    authors_data = json.load(f)

with open('quotes.json', 'r') as f:
    quotes_data = json.load(f)

save_authors(authors_data)
authors_dict = {author['fullname']: author for author in authors_data}
save_quotes(quotes_data, authors_dict)