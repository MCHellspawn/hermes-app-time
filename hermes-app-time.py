"""Skill to tell you the time."""
import logging
import random
import pytz
from datetime import datetime
from zoneinfo import ZoneInfo
from rhasspyhermes.nlu import NluIntent
from rhasspyhermes_app import EndSession, HermesApp

_LOGGER = logging.getLogger("TimeApp")

app = HermesApp("TimeApp")

def get_time_response_sentence(intent: NluIntent, time: datetime):
    _LOGGER.debug(f"Intent: {intent.id} | Started get_time_response_sentence")
    # open the responses file in read mode
    responsesfile = open("config/responses.txt", "r")
  
    # reading the file
    responsesdata = responsesfile.read()
    responseslist = responsesdata.split("\n")

    if (time.strftime("%M") == "0"):
        time_string = time.strftime("%I o clock")
    elif (time.strftime("%M")[0:1] == "0"):
        time_string = time.strftime("%I o %M %p")
    else:
        time_string = time.strftime("%I %M %p")
    
    sentence = random.choice(responseslist).format(time_string)
    #sentence = f"It's {time_string}"
    _LOGGER.debug(f"Intent: {intent.id} | get_time_response_sentence sentence: {sentence}")
    _LOGGER.debug(f"Intent: {intent.id} | Completed get_time_response_sentence")
    return sentence

def diff_hours_tz(from_tz_name, to_tz_name, negative=False):
    from_tz = pytz.timezone(from_tz_name)
    to_tz = pytz.timezone(to_tz_name)

    utc_dt = datetime.now(datetime.tzinfo(ZoneInfo(str(from_tz))))
    dt_from = dt_to = datetime.utcnow()

    dt_from = from_tz.localize(dt_from)
    dt_to = to_tz.localize(dt_to)

    from_d = dt_from - utc_dt
    if from_d.days < 0:
        return diff_hours_tz(to_tz_name, from_tz_name, True)

    dt_delta = dt_from - dt_to

    negative_int = -1 if negative else 1

    return int(dt_delta.seconds/3600)*negative_int

@app.on_intent("TimeGetTime")
async def get_time(intent: NluIntent):
    """Tell the time."""
    _LOGGER.info(f"Intent: {intent.id} | Started: TimeGetTime")
    # Check if the timezone slot was sent
    if any(slot for slot in intent.slots if slot.slot_name == 'timezone'):
        # Get the timezone slot
        timezoneslot = next((slot for slot in intent.slots if slot.slot_name == 'timezone'), None)
        _LOGGER.info(f"Intent: {intent.id} | Timezone slot: {timezoneslot}")
        # Build the timezone object and convert the time
        tzobject = pytz.timezone(timezoneslot.value['value'])
        now = datetime.now(tzobject)        
        _LOGGER.info(f"Intent: {intent.id} | Date/Time: {now}")
        # Generate the response sentence
        sentence = get_time_response_sentence(intent, now)
    else:
        _LOGGER.info(f"Intent: {intent.id} | Timezone slot empty")
        # Get the time
        now = datetime.now()
        _LOGGER.info(f"Intent: {intent.id} | Date/Time: {now}")
        # Generate the response sentence
        sentence = get_time_response_sentence(intent, now)
       
    _LOGGER.info(f"Intent: {intent.id} | Responded to TimeGetTime")
    _LOGGER.info(f"Intent: {intent.id} | Sentence: {sentence}")
    _LOGGER.info(f"Intent: {intent.id} | Completed: TimeGetTime")
    return EndSession(sentence)

@app.on_intent("TimeTzDiff")
async def get_tz_difference(intent: NluIntent):
    _LOGGER.info(f"Intent: {intent.id} | Completed: TimeTzxDiff")
    timezone1slot = next((slot for slot in intent.slots if slot.slot_name == 'timezone1'), None)
    timezone2slot = next((slot for slot in intent.slots if slot.slot_name == 'timezone2'), None)

    hours = diff_hours_tz(timezone1slot.value['value'],timezone2slot.value['value'])
    _LOGGER.info(f"Intent: {intent.id} | Difference in hours: {hours}")

    _LOGGER.info(f"Intent: {intent.id} | Completed: TimeTzxDiff")
    return EndSession("The time differnece is 1 hour")

if __name__ == "__main__":
    _LOGGER.info("Starting Hermes App: Time")
    app.run()