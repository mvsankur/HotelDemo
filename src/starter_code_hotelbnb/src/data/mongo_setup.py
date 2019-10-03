import mongoengine
from mongoengine import connect
DEFAULT_CONNECTION_NAME = connect('hotel_holiday_inn')


def global_init():
    mongoengine.register_connection(alias='core', name='hotel_holiday_inn')