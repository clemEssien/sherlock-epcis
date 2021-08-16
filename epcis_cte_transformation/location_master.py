from tools.serializer import jsonid, map_from_json, map_to_json
import json

from epcis_cte_transformation.cte import CTEBase
from epcis_cte_transformation.creation_cte import CreationCTE
from epcis_cte_transformation.growing_cte import GrowingCTE
from epcis_cte_transformation.receiving_cte import ReceivingCTE
from epcis_cte_transformation.shipping_cte import ShippingCTE
from epcis_cte_transformation.transformation_cte import TransformationCTE

from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.worksheet import Worksheet

# export const locationMasterOliveRows = [
# {
# "locationId": "9991002100014", //Receiving (receiver_location_identifier), Creation(location_where_food_was_created), Shipping(location_of_source_of_shipment), Transformation(location_of_transformation), Growing (growing_location)
# "businessName": "Olive Oil Company", //Not Found
# "physicalLocationName": "Olive Oil Company", // Not found
# "phone": "111.111.1111", //Receiving (point_of_contact_phone)
# "address": "100 Italy", //Not Found
# "city": "Italy", //Not Found
# "state": "Italy", //Not Found
# "zip": "10000" //Not Found
# },
# ];

    
loc_map = {
    "locationId": [
        {
            "types": [ ReceivingCTE ],
            "key": "receiverLocationIdentifier"
        },
        {
            "types": [ CreationCTE ],
            "key": "locationWhereFoodWasCreated"
        },
        {
            "types": [ ShippingCTE ],
            "key": "locationOfSourceOfShipment"
        },
        {
            "types": [ TransformationCTE ],
            "key": "locationOfTransformation"
        },
        {
            "types": [ GrowingCTE ],
            "key": "growingLocation"
        },
    ],
    "phone": [
        {
            "types": [ ReceivingCTE ],
            "key": "pointOfContactPhone"
        }
    ]
}

def get_map_from_type(key, type):
    if not key in loc_map:
        return None
    map = loc_map[key]
    if not map:
        return None
    for cte in map:
        for cte_type in cte["types"]:
            if type == cte_type:
                return cte["key"]
    
    return None
    

class LocationMaster:
      
    @classmethod
    def new_from_cte(cls, cte):
        result = cls()
        search = type(cte)
        
        data1 = map_to_json(cte)
        data2 = map_to_json(result)
        
        for key in data2.keys():
            newkey = get_map_from_type(key, search)
            if newkey and newkey in data1:
                data2[key] = data1[newkey]

        map_from_json(data2, result)
        return result
    
    def __init__(self) -> None:
        self._location_id: str = ""
        self._business_name: str = ""
        self._physical_location_name: str = ""
        self._phone: str = ""
        self._address: str = ""
        self._city: str = ""
        self._state: str = ""
        self._zip: str = ""
        
    @property
    @jsonid("locationId")
    def location_id(self) -> str:
        return self._location_id
    
    @location_id.setter
    def location_id(self, value: str) -> None:
        self._location_id = value

    @property
    @jsonid("businessName")
    def business_name(self) -> str:
        return self._business_name
    
    @business_name.setter
    def business_name(self, value: str) -> None:
        self._business_name = value

    @property
    @jsonid("physicalLocationName")
    def physical_location_name(self) -> str:
        return self._physical_location_name
    
    @physical_location_name.setter
    def physical_location_name(self, value: str) -> None:
        self._physical_location_name = value

    @property
    @jsonid("phone")
    def phone(self) -> str:
        return self._phone
    
    @phone.setter
    def phone(self, value: str) -> None:
        self._phone = value

    @property
    @jsonid("address")
    def address(self) -> str:
        return self._address
    
    @address.setter
    def address(self, value: str) -> None:
        self._address = value

    @property
    @jsonid("city")
    def city(self) -> str:
        return self._city
    
    @city.setter
    def city(self, value: str) -> None:
        self._city = value

    @property
    @jsonid("state")
    def state(self) -> str:
        return self._state
    
    @state.setter
    def state(self, value: str) -> None:
        self._state = value

    @property
    @jsonid("zip")
    def zip(self) -> str:
        return self._zip
    
    @zip.setter
    def zip(self, value: str) -> None:
        self._zip = value

    def output_xlsx(self, sheet, row):
        pass
