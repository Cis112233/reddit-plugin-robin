from datetime import datetime

from pylons import app_globals as g

from r2.lib.eventcollector import Event

EVENT_TOPIC = "robin_events"


def _age_in_ms(room):
    age = datetime.now(g.tz) - room.date
    age_in_ms = (age.seconds * 1000) + (age.microseconds / 1000)
    return age_in_ms


def message(room, message, sent_dt, request=None, context=None):
    """Create and save a 'message' event.

    room: a RobinRoom object
    message: A string, <= 140 characters, representing the message sent
    send_dt: A datetime object, representing when the message was sent
    request, context: pylons.request & pylons.c respectively

    """
    event = Event(
        topic=EVENT_TOPIC,
        event_type="ss.robin_message",
        time=sent_dt,
        request=request,
        context=context,
    )

    event.add("room_id", room._id)
    event.add("room_age", _age_in_ms(room))
    event.add_text("message_body", message)

    g.events.save_event(event)
