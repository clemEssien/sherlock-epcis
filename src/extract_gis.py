import datetime
import json
from uuid import UUID


def map_from_epcis(data, obj):
    """Map data from a data dictionary  to a class object instance's data attributes.

    Args:
        data: Any
            Json Map file
        obj: Any
            The class object to load the data in to
    """
    if data is None:
        return None

    epcis_json = data["attr_key_mapping"]

    for attr in epcis_json.keys():
        setattr(obj, attr, epcis_json[attr])
    return obj

