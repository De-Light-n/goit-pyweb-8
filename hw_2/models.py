import configparser
import pathlib
from mongoengine import Document, connect, StringField, BooleanField, IntField


file_config = pathlib.Path(__file__).parent.parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_config)

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
domain = config.get('DB', 'domain')

connect(db="Pub_Sub",
        host=f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/")

class Task(Document):
    name = StringField(max_length=50, required=True)
    age = IntField(min_value=10, max_value=75)
    email = StringField()
    phone = StringField(max_length=30)
    preferred_method = StringField()
    completed = BooleanField(default=False)
    
