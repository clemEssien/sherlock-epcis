# Author: Kevin Zong
# Last Modified: June 27th, 2021
# Class representing Receiving CTE/KDE data

from abc import ABC, abstractclassmethod, abstractmethod
from typing import List, Type
import os, sys

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from JSONDeserialization.epcis_event import (
    QuantityElement,
    QuantityEvent,
    URI,
    CommonEvent,
    AggregationEvent,
    EPCISEvent,
    ObjectEvent,
    TransactionEvent,
    TransformationEvent,
)
from cte import CTEBase
import json
import datetime


class ReceivingCTE:
    """
    Provides a class for the Receiving CTE and defines its KDEs

    KDEs:
            Reference Record Number : str
            Transporter Name : str
            Entry Number : str
            Traceability Lot Code : List
            Quantity Received : List
            Unit of Measure : List
            Traceability Product : List
            Lot Code Generator Location : str
            Point of Contact Name : str
            Point of Contact Phone : str
            Point of Contact Email : str
            Receiver Location Identifier : str
            Immediate Previous Source Location Identifier : str
            Receipt Time : datetime
    """

    def __init__(self):
        self._reference_record_number = ""
        self._transporter_name = ""
        self._entry_number = ""
        self._traceability_lot_code = []
        self._quantity_received = []
        self._unit_of_measure = []
        self._traceability_product = []
        self._lot_code_generator_location = ""
        self._point_of_contact_name = ""
        self._point_of_contact_phone = ""
        self._point_of_contact_email = ""
        self._receiver_location_identifier = ""
        self._previous_source = ""
        self._receipt_time: datetime.datetime(1,1,1)
        
    def new_from_data(cls, data: dict):
        pass

    def new_from_epcis(cls, event: EPCISEvent):
        output = cls()

        output.receipt_time = event.event_time_local
        
        

        return output

    def new_from_json(cls, json_data: str):
        data = json.loads(json_data)
        return cls.new_from_data(data)

    def new_from_excel(cls, excel_data: str):
        pass

    def save_to_excel(self):
        pass

    def new_from_csv(cls, csv_lines: "list[str]"):
        pass

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
        
    def output_json(self) -> str:
        pass
    
    def output_xlsx(self) -> str:
        """
        Create an excel spreadsheet and output the contents to an XML string
        """

        # code here

        v = "foobar"
        return v

    def save_as_xlsx(self, filename: str):
        pass
        # code here