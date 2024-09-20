from mongoengine import Document, connect, StringField, BooleanField, IntField

connect(db="Pub_Sub",
        host="mongodb+srv://Dlite:*****@cluster0.4m1kv.mongodb.net/")

class Task(Document):
    name = StringField(max_length=50, required=True)
    age = IntField(min_value=10, max_value=75)
    email = StringField()
    phone = StringField(max_length=30)
    preferred_method = StringField()
    completed = BooleanField(default=False)
    
