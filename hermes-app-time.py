"""Skill to tell you the time."""
import logging
from datetime import datetime
from rhasspyhermes.nlu import NluIntent
from rhasspyhermes_app import EndSession, HermesApp

_LOGGER = logging.getLogger("TimeApp")

app = HermesApp("TimeApp")

def get_time_response_sentence(time: datetime):
    if (time.strftime("%M")[0:1] == "0"):
        time_string = time.strftime("%I o %M %p")
    else:
        time_string = time.strftime("%I %M %p")

    sentence = f"It's {time_string}"
    return sentence

@app.on_intent("GetTime")
async def get_time(intent: NluIntent):
    """Tell the time."""
    now = datetime.now()
    
    sentence = get_time_response_sentence(now)
       
    _LOGGER.info("Responded to GetTime")
    _LOGGER.info(sentence)
    return EndSession(sentence)

if __name__ == "__main__":
    _LOGGER.info("Starting Hermes App: Time")
    app.run()