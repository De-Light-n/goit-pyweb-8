
from mongoengine import connect, Document, ReferenceField, StringField, ListField, CASCADE


connect(db="authors_and_quotes",
        host="mongodb+srv://Dlite:*****@cluster0.4m1kv.mongodb.net/")

class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=30)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}
    
class Quote(Document):
    quote = StringField()
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=20))
    meta = {"collection": "quotes"}
    
