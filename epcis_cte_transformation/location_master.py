from tools.serializer import jsonid, map_from_json, map_to_json
import json

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
class LocationMaster:
    
    def __init__(self) -> None:
        self._location_id: str = None
        self._business_name: str = None
        self._physical_location_name: str = None
        self._phone: str = None
        self._address: str = None
        self._city: str = None
        self._state: str = None
        self._zip: str = None
        
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
