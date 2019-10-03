import datetime
import mongoengine


class People(mongoengine.Document):
    registered_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    sex = mongoengine.StringField(required=True)

    age = mongoengine.FloatField(required=True)
    name = mongoengine.StringField(required=True)
    is_adult = mongoengine.BooleanField(required=True)

    meta = {
        'db_alias': 'core',
        'collection': 'peoples'
    }