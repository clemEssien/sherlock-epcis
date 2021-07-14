import os, sys

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
from JSONDeserialization.epcis_event import (
    EPCISEvent,
    URI,
)


class CTEDetector:
    """Class to determine which FDA CTE an EPCIS event corresponds with.

    Attributes:
        event_chars : dict
            A dictionary identifying each FDA CTE by expected characteristics of an EPCIS event.
    """

    def __init__(self, event_chars: dict = None) -> None:
        self._event_chars: dict = event_chars

    @property
    def event_chars(self) -> dict:
        return self._event_chars

    @event_chars.setter
    def event_chars(self, value: dict) -> None:
        self._event_chars = value

    def detect_cte(self, epcis_event: EPCISEvent) -> str:
        """Return the most likely CTE for a given epcis_event"""
        # Calculate the number of characteristics the event shares with each CTE
        valid_ctes = [key for key in self._event_chars if self._event_chars[key]]
        cte_bins = dict.fromkeys(valid_ctes, 0)
        for cte in valid_ctes:
            for element in self._event_chars[cte].keys():
                if element == "event_type":
                    for event_name in self._event_chars[cte][element]:
                        if epcis_event.__class__.__name__ == event_name:
                            cte_bins[cte] += 1
                else:
                    for possible_val in self._event_chars[cte][element]:
                        attr_val = getattr(epcis_event, element)
                        if isinstance(attr_val, URI):
                            if attr_val.value:
                                if attr_val.value == possible_val:
                                    cte_bins[cte] += 1
                            else:
                                if possible_val in attr_val.uri_str:
                                    cte_bins[cte] += 1
                        elif isinstance(attr_val, str):
                            if possible_val in attr_val:
                                cte_bins[cte] += 1
                        else:
                            raise (
                                "detectable EPCISEvent properties must be URIs or strings"
                            )
        # Return the CTE with the highest percentage of shared characteristics
        for cte in cte_bins.keys():
            cte_bins[cte] /= len(self._event_chars[cte])
        return max(cte_bins, key=lambda cte: cte_bins[cte])
