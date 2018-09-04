import datetime
from mongoengine import Document, StringField, DateTimeField

class AR_Models_Handler(Document):
    model_path = StringField(required=True)
    business_id = StringField(required=True)
    date_created = DateTimeField(default=datetime.datetime.utcnow)