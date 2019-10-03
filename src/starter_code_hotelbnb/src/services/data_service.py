from typing import List, Optional

import datetime

import bson

from data.bookings import Booking
from data.rooms import Room
from data.owners import Owner
from data.peoples import People


def create_account(name: str, email: str) -> Owner:
    owner = Owner()
    owner.name = name
    owner.email = email

    owner.save()

    return owner


def find_account_by_email(email: str) -> Owner:
    owner = Owner.objects(email=email).first()
    return owner


def register_room(active_account: Owner,
                  name, allow_dangerous, has_toys,
                  carpeted, meters, price) -> Room:
    room = Room()

    room.name = name
    room.square_meters = meters
    room.is_carpeted = carpeted
    room.has_toys = has_toys
    room.allow_adult_people = allow_dangerous
    room.price = price

    cage.save()

    account = find_account_by_email(active_account.email)
    account.room_ids.append(room.id)
    account.save()

    return room


def find_room_for_user(account: Owner) -> List[Room]:
    query = Room.objects(id__in=account.room_ids)
    rooms = list(query)

    return rooms


def add_available_date(room: Room,
                       start_date: datetime.datetime, days: int) -> Room:
    booking = Booking()
    booking.check_in_date = start_date
    booking.check_out_date = start_date + datetime.timedelta(days=days)

    room = Room.objects(id=room.id).first()
    room.bookings.append(booking)
    room.save()

    return room


def add_people(account, name, age, sex, is_adult) -> People:
    people = People()
    people.name = name
    people.age = age
    people.sex = sex
    people.is_adult = is_adult
    people.save()

    owner = find_account_by_email(account.email)
    owner.people_ids.append(people.id)
    owner.save()

    return people


def get_people_for_user(user_id: bson.ObjectId) -> List[People]:
    owner = Owner.objects(id=user_id).first()
    peoples = People.objects(id__in=owner.people_ids).all()

    return list(peoples)


def get_available_rooms(checkin: datetime.datetime,
                        checkout: datetime.datetime, people: People) -> List[Room]:
    min_size = people.length / 4

    query = Room.objects() \
        .filter(square_meters__gte=min_size) \
        .filter(bookings__check_in_date__lte=checkin) \
        .filter(bookings__check_out_date__gte=checkout)

    if snake.is_venomous:
        query = query.filter(allow_adult_people=True)

    cages = query.order_by('price', '-square_meters')

    final_rooms = []
    for c in rooms:
        for b in c.bookings:
            if b.check_in_date <= checkin and b.check_out_date >= checkout and b.guest_snake_id is None:
                final_rooms.append(c)

    return final_rooms


def book_room(account, people, room, checkin, checkout):
    booking: Optional[Booking] = None

    for b in room.bookings:
        if b.check_in_date <= checkin and b.check_out_date >= checkout and b.guest_snake_id is None:
            booking = b
            break

    booking.guest_owner_id = account.id
    booking.guest_people_id = people.id
    booking.check_in_date = checkin
    booking.check_out_date = checkout
    booking.booked_date = datetime.datetime.now()

    room.save()


def get_bookings_for_user(email: str) -> List[Booking]:
    account = find_account_by_email(email)

    booked_cages = Cage.objects() \
        .filter(bookings__guest_owner_id=account.id) \
        .only('bookings', 'name')

    def map_room_to_booking(cage, booking):
        booking.room = room
        return booking

    bookings = [
        map_room_to_booking(room, booking)
        for room in booked_rooms
        for booking in room.bookings
        if booking.guest_owner_id == account.id
    ]

    return bookings