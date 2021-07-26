import os, sys
import yaml
import json

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
        _non_attribute_handlers : dict
            A dictionary mapping the non_attribute characteristics to their handler functions.
    """

    def __init__(self, event_characteristics: dict = None) -> None:
        self._event_characteristics: dict = event_characteristics
        self._non_attribute_handlers = {"event_type": "_event_type_handler"}

    @property
    def event_chars(self) -> dict:
        return self._event_characteristics

    @event_chars.setter
    def event_chars(self, value: dict) -> None:
        self._event_characteristics = value

    def import_yaml_file(self, filename: str) -> None:
        """Set event_chars to content of a given yaml file"""
        with open(filename, "r") as f:
            try:
                detection_config = yaml.safe_load(f)
            except:
                raise ValueError("File must follow the YAML format.")
            self._event_characteristics = detection_config

    def import_json_file(self, filename: str) -> None:
        """Set event_chars to content of a given json file"""
        with open(filename, "r") as f:
            try:
                detection_config = json.load(f)
            except:
                raise ValueError("File must follow the JSON format.")
            self._event_characteristics = detection_config

    def _event_type_handler(
        self, epcis_event: EPCISEvent, cte: str, cte_bins: dict
    ) -> None:
        """Handler to determine if given event has the given event_type characteristic"""
        for event_name in self._event_characteristics[cte]["non_attributes"]["event_type"]:
            cte_bins[cte] += epcis_event.__class__.__name__ == event_name

    def detect_cte(self, epcis_event: EPCISEvent) -> str:
        """Return the most likely CTE for a given epcis_event"""
        if not isinstance(epcis_event, EPCISEvent):
            raise TypeError(
                "Invalid data type. Must be an EPCISEvent or subclass of an EPCISEvent."
            )
        # Calculate the number of characteristics the event shares with each CTE
        valid_ctes = [key for key in self._event_characteristics if self._event_characteristics[key]]
        cte_bins = dict.fromkeys(valid_ctes, 0)
        for cte in valid_ctes:
            for char_type in self._event_characteristics[cte].keys():
                if char_type == "non_attributes":
                    for non_attr_char in self._event_characteristics[cte][char_type].keys():
                        handler = getattr(
                            self, self._non_attribute_handlers[non_attr_char]
                        )
                        handler(epcis_event, cte, cte_bins)
                elif char_type == "event_attributes":
                    for element in self._event_characteristics[cte][char_type].keys():
                        for possible_val in self._event_characteristics[cte][char_type][element]:
                            try:
                                attr_val = getattr(epcis_event, element)
                            except:
                                raise Exception("Attribute does not exist")
                            if str(attr_val) == "":
                                continue
                            if isinstance(attr_val, URI):
                                if attr_val._is_split:
                                    if attr_val.value == possible_val:
                                        cte_bins[cte] += 1
                                    elif possible_val[0] == attr_val.value[0]:
                                        # See if they at least share the first letter, then get the length of the
                                        # common prefix to catch things like ship, shipment, shipped when the event_char is shipping
                                        prefix_len = len(
                                            os.path.commonprefix(
                                                [attr_val.value, possible_val]
                                            )
                                        )
                                        cte_bins[cte] += prefix_len / len(possible_val)
                                else:
                                    if possible_val in attr_val.uri_str:
                                        cte_bins[cte] += 1
                                    elif possible_val[0] == attr_val.uri_str[0]:
                                        prefix_len = len(
                                            os.path.commonprefix(
                                                [attr_val.uri_str, possible_val]
                                            )
                                        )
                                        cte_bins[cte] += prefix_len / len(possible_val)
                            elif isinstance(attr_val, str):
                                if possible_val == attr_val:
                                    cte_bins[cte] += 1
                                elif possible_val[0] == attr_val[0]:
                                    prefix_len = len(
                                        os.path.commonprefix([attr_val, possible_val])
                                    )
                                    cte_bins[cte] += prefix_len / len(possible_val)
        # Return the CTE with the highest percentage of shared characteristics
        for cte in cte_bins.keys():
            cte_bins[cte] /= len(self._event_characteristics[cte])
        return max(cte_bins, key=lambda cte: cte_bins[cte])
