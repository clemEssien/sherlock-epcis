from JSONDeserialization.epcis_event import EPCISEvent
import json
from sys import settrace


class CTEDetector:
    """Class to determine which FDA CTE an EPCIS event corresponds with.

    Attributes:
        cte_list : list
            List of FDA CTEs that an EPCIS event can correspond to.
        event_chars : dict
            A dictionary identifying each FDA CTE by expected characteristics of an EPCIS event.
    """

    cte_list = [
        "growing",
        "growing_sprouts",
        "creation",
        "transformation",
        "shipping",
        "receiving",
        "receiving_first_non_fishing_vessel",
        "receiving_first_fishing_vessel",
    ]

    def __init__(self, event_chars: dict = None) -> None:
        self._event_chars: dict = event_chars

    @property
    def event_chars(self) -> dict:
        return self._event_chars

    @event_chars.setter
    def event_chars(self, value: dict):
        self._event_chars = value

    def detect_cte(epcis_event: EPCISEvent) -> str:
        pass
