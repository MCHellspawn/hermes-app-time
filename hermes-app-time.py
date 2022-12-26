"""Skill to tell you the time."""
import logging
import random
from datetime import datetime
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
    
    if (time.strftime("%M")[0:1] == "0"):
        time_string = time.strftime("%I o %M %p")
    else:
        time_string = time.strftime("%I %M %p")
    
    sentence = random.choice(responseslist).format(time_string)
    #sentence = f"It's {time_string}"
    _LOGGER.debug(f"Intent: {intent.id} | get_time_response_sentence sentence: {sentence}")
    _LOGGER.debug(f"Intent: {intent.id} | Completed get_time_response_sentence")
    return sentence

@app.on_intent("TimeGetTime")
async def get_time(intent: NluIntent):
    """Tell the time."""
    _LOGGER.info(f"Intent: {intent.id} | Started: TimeGetTime")
    now = datetime.now()
    
    sentence = get_time_response_sentence(intent, now)
       
    _LOGGER.info(f"Intent: {intent.id} | Responded to TimeGetTime")
    _LOGGER.info(f"Intent: {intent.id} | Sentence {sentence}")
    _LOGGER.info(f"Intent: {intent.id} | Completed: TimeGetTime")
    return EndSession(sentence)

if __name__ == "__main__":
    _LOGGER.info("Starting Hermes App: Time")
    app.run()