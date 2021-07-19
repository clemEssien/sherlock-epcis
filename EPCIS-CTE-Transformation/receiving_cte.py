# Author: Kevin Zong
# Last Modified: June 19th, 2021
# Class representing Receiving CTE/KDE data

from _typeshed import Self
from JSONDeserialization import epcis_event
import datetime


class ReceivingCte:
    def __init__(self):
        self._reference_record_number
        self._transporter_name
        self._entry_number: str = ""
        self._traceability_lot_code: str = ""
        self._quantity_received: list[float] = []
        self._unit_of_measure: list[str] = []
        self._traceability_product: str = ""
        self._lot_code_generator_location
        self._point_of_contact_name
        self._point_of_contact_phone
        self._point_of_contact_email
        self._receiver_location_identifier: str = ""
        self._previous_source: str = ""
        self._receipt_time: datetime.datetime(1,1,1)
        self._receipt_timezone_offset: datetime.timezone(datetime.timedelta(hours=0))
        
        
    @property
    def reference_record_number(self) -> str:
        return self._reference_record_number

    @reference_record_number.setter
    def reference_record_number(self, value: str):
        self._reference_record_number = value    
        
    @property
    def transporter_name(self) -> str:
        return self._transporter_name

    @transporter_name.setter
    def transporter_name(self, value: str):
        self._transporter_name = value    
        
    @property
    def entry_number(self) -> str:
        return self._entry_number

    @entry_number.setter
    def entry_number(self, value: str):
        self._entry_number = value

    @property
    def traceability_lot_code(self) -> str:
        return self._traceability_lot_code

    @traceability_lot_code.setter
    def traceability_lot_code(self, value: str):
        self._traceability_lot_code = value

    @property
    def quantity_received(self) -> str:
        return self._quantity_received

    @quantity_received.setter
    def quantity_received(self, value: str):
        self._quantity_received = value

    @property
    def unit_of_measure(self) -> str:
        return self._unit_of_measure

    @unit_of_measure.setter
    def unit_of_measure(self, value: str):
        self._unit_of_measure = value

    @property
    def traceability_product(self) -> str:
        return self._traceability_product

    @traceability_lot_code.setter
    def traceability_product(self, value: str):
        self._traceability_product = value

    @property
    def lot_code_generator_location(self) -> str:
        return self._lot_code_generator_location

    @lot_code_generator_location.setter
    def lot_code_generator_location(self, value: str):
        self._lot_code_generator_location = value
    
    @property
    def point_of_contact_name(self) -> str:
        return self._point_of_contact_name

    @point_of_contact_name.setter
    def point_of_contact_name(self, value: str):
        self._point_of_contact_name = value

    @property
    def point_of_contact_phone(self) -> str:
        return self._point_of_contact_phone

    @point_of_contact_phone.setter
    def point_of_contact_phone(self, value: str):
        self._point_of_contact_phone = value

    @property
    def point_of_contact_email(self) -> str:
        return self._point_of_contact_email

    @point_of_contact_email.setter
    def point_of_contact_email(self, value: str):
        self._point_of_contact_email = value   

    @property
    def receiver_location_identifier(self) -> str:
        return self._receiver_location_identifier

    @receiver_location_identifier.setter
    def receiver_location_identifier(self, value: str):
        self._receiver_location_identifier = value

    @property
    def previous_source(self) -> str:
        return self._previous_source

    @previous_source.setter
    def previous_sorce(self, value: str):
        self._previous_source = value  

    @property
    def receipt_time(self) -> str:
        return self._receipt_time

    @receipt_time.setter
    def receipt_time(self, value: str):
        self._receipt_time = value

    @property
    def receipt_timezone_offset(self) -> str:
        return self._receipt_timezone_offset

    @receipt_timezone_offset.setter
    def receipt_timezone_offset(self, value: str):
        self._receipt_timezone_offset = value    
    
    