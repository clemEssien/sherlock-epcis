from pathlib import Path
import sys

# Pylance doesn't love this, but it works.
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
from src import epcis_event

test_event = epcis_event.EPCISEvent()
test_event.event_time = "6-14-2021 9:36PM EDT"
test_event.event_timezone_offset = "-04:00"
print("Non-ISO Input:")
print("UTC:  ", test_event.event_time)
print("Local:", test_event.event_time_local)
print("ISO Input:")
test_event.event_time = "2005-07-11T11:30:47+00:00"
print("UTC:  ", test_event.event_time)
print("Local:", test_event.event_time_local)
