# Author: Kevin Zong
# Last Modified: August 13th, 2021
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
from epcis_cte_transformation.cte import CTEBase
import json
import datetime
from tools.serializer import jsonid
#from openpyxl import Workbook, load_workbook
from tools.serializer import JSONValueProvider, jsonid, map_from_json, map_to_json

class ReceivingCTE:
    """
    Provides a class for the Receiving CTE and defines its KDEs

    KDEs:
            Reference Record Number : str
            Transporter Name : str
            Entry Number : str
            Traceability Lot Code : List[str]
            Quantity Received : List[str]
            Unit of Measure : List[str]
            Traceability Product : List[str]
            Lot Code Generator Location : str
            Point of Contact Name : str
            Point of Contact Phone : str
            Point of Contact Email : str
            Receiver Location Identifier : str
            Immediate Previous Source Location Identifier : str
            Receipt Time : datetime

            ---First Receiver---
            Traceability Lot Code : List[str]
            Location of Originator : str
            Point of Contact Name : str
            Point of Contact Phone : str
            Point of Contact Email : str
            Date and Time of Harvesting : datetime
            Location of Food Cooling : str
            Date and time of Food Cooling : datetime
            Location of Food Packing : str
            Date and time of Food Packing : datetime

            ---First Receiver from a Fishing Vessel---
            Traceability Lot Code : List[str]
            Harvest Date for the Trip during which seafood was caught: datetime
            Location(s) for the Trip during which seafood was caught: str
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

        self._receipt_time = datetime.datetime(1,1,1)
        self._harvest_date = datetime.datetime(1,1,1)
        self._cooling_location = ""
        self._cooling_date = datetime.datetime(1,1,1)
        self._packing_location = ""
        self._packing_date = datetime.datetime(1,1,1)
        self._catch_location = []

    @classmethod    
    def new_from_data(cls, data: dict):
        pass

    @classmethod 
    def new_from_epcis(cls, event: EPCISEvent):
        output = cls()
        try:
            output.receipt_time = event.event_time_local
        except ValueError:
            output.receipt_time = "" 
        if(issubclass(type(event), CommonEvent)):
            try:
                #print("Previous Source: " + event.source_list[0].get("source").value)
                for sour in event.source_list:
                    output.previous_source = sour.get("source").value
            except ValueError:
                    output.previous_source = ""
            try:
                output.receiver_location_identifier = event.read_point.value
            except ValueError:
                output.receiver_location_identifier = ""
        if isinstance(event, ObjectEvent):
            for qe in event.quantity_list:
                output.quantity_received.append(qe.quantity)
                output.unit_of_measure.append(qe.uom)
                output.traceability_lot_code.append(qe.epc_class.value)
            for epc in event.epc_list:
                output.traceability_product.append(epc.value)
        elif isinstance(event, AggregationEvent):
            for qe in event.child_quantity_list:
                output.quantity.append(qe.quantity)
                output.unit_of_measure.append(qe.uom)
                output.traceability_lot_code.append(qe.epc_class.value)
            for epc in event.child_epc_list:
                output.traceability_product.append(epc.value)
        elif isinstance(event, TransactionEvent):
            for qe in event.quantity_list:
                output.quantity.append(qe.quantity)
                output.unit_of_measure.append(qe.uom)
                output.traceability_lot_code.append(qe.epc_class.value)
            for epc in event.epc_list:
                output.traceability_product.append(epc.value)
        elif isinstance(event, TransformationEvent):
            for qe in event.input_quantity_list:
                output.quantity.append(qe.quantity)
                output.unit_of_measure.append(qe.uom)
                output.traceability_lot_code.append(qe.epc_class.value)
            for epc in event.input_epc_list:
                output.traceability_product.append(epc.value)
        return output

    @classmethod 
    def new_from_json(cls, json_data: str):
        data = json.loads(json_data)
        return cls.new_from_data(data)

    @classmethod 
    def new_from_excel(cls, excel_data: str):
        pass

    @classmethod 
    def save_to_excel(self):
        pass

    @classmethod 
    def new_from_csv(cls, csv_lines: "list[str]"):
        pass

    @property
    @jsonid("referenceRecordNumber")
    def reference_record_number(self) -> str:
        return self._reference_record_number

    @reference_record_number.setter
    def reference_record_number(self, value: str):
        self._reference_record_number = value    
        
    @property
    @jsonid("transporterName")
    def transporter_name(self) -> str:
        return self._transporter_name

    @transporter_name.setter
    def transporter_name(self, value: str):
        self._transporter_name = value    
        
    @property
    @jsonid("entryNumber")
    def entry_number(self) -> str:
        return self._entry_number

    @entry_number.setter
    def entry_number(self, value: str):
        self._entry_number = value

    @property
    @jsonid("traceabilityLotCode")
    def traceability_lot_code(self) -> List:
        return self._traceability_lot_code

    @traceability_lot_code.setter
    def traceability_lot_code(self, value: List):
        self._traceability_lot_code = value

    @property
    @jsonid("quantityReceived")
    def quantity_received(self) -> List:
        return self._quantity_received

    @quantity_received.setter
    def quantity_received(self, value: List):
        self._quantity_received = value

    @property
    @jsonid("unit")
    def unit_of_measure(self) -> List:
        return self._unit_of_measure

    @unit_of_measure.setter
    def unit_of_measure(self, value: List):
        self._unit_of_measure = value

    @property
    @jsonid("traceabilityProduct")
    def traceability_product(self) -> List:
        return self._traceability_product

    @traceability_product.setter
    def traceability_product(self, value: List):
        self._traceability_product = value

    @property
    @jsonid("lotCodeGeneratorLocation")
    def lot_code_generator_location(self) -> str:
        return self._lot_code_generator_location

    @lot_code_generator_location.setter
    def lot_code_generator_location(self, value: str):
        self._lot_code_generator_location = value
    
    @property
    @jsonid("pointOfContactName")
    def point_of_contact_name(self) -> str:
        return self._point_of_contact_name

    @point_of_contact_name.setter
    def point_of_contact_name(self, value: str):
        self._point_of_contact_name = value

    @property
    @jsonid("pointOfContactPhone")
    def point_of_contact_phone(self) -> str:
        return self._point_of_contact_phone

    @point_of_contact_phone.setter
    def point_of_contact_phone(self, value: str):
        self._point_of_contact_phone = value

    @property
    @jsonid("pointOfContactEmail")
    def point_of_contact_email(self) -> str:
        return self._point_of_contact_email

    @point_of_contact_email.setter
    def point_of_contact_email(self, value: str):
        self._point_of_contact_email = value   

    @property
    @jsonid("receiverLocationIdentifier")
    def receiver_location_identifier(self) -> str:
        return self._receiver_location_identifier

    @receiver_location_identifier.setter
    def receiver_location_identifier(self, value: str):
        self._receiver_location_identifier = value

    @property
    @jsonid("previousSource")
    def previous_source(self) -> str:
        return self._previous_source

    @previous_source.setter
    def previous_source(self, value: str):
        self._previous_source = value  

    @property
    @jsonid("receiptTime")
    def receipt_time(self) -> datetime.datetime:
        return self._receipt_time

    @receipt_time.setter
    def receipt_time(self, value: datetime.datetime):
        self._receipt_time = value

    @property
    @jsonid("harvestDate")
    def harvest_date(self) -> datetime.datetime:
        return self._harvest_date

    @harvest_date.setter
    def harvest_date(self, value: datetime.datetime):
        self._harvest_date = value   

    @property
    @jsonid("coolingLocation")
    def cooling_location(self) -> str:
        return self._cooling_location

    @cooling_location.setter
    def cooling_location(self, value: str):
        self._cooling_location = value

    @property
    @jsonid("coolingDate")
    def cooling_date(self) -> datetime.datetime:
        return self._cooling_date

    @cooling_date.setter
    def cooling_date(self, value: datetime.datetime):
        self._cooling_date = value

    @property
    @jsonid("packingLocation")
    def packing_location(self) -> str:
        return self._packing_location

    @packing_location.setter
    def packing_location(self, value: str):
        self._packing_location = value

    @property
    @jsonid("packingDate")
    def packing_date(self) -> datetime.datetime:
        return self._packing_date

    @packing_date.setter
    def packing_date(self, value: datetime.datetime):
        self._packing_date = value   

    @property
    @jsonid("catchLocation")
    def catch_location(self) -> List:
        return self._catch_location

    @catch_location.setter
    def catch_location(self, value: List):
        self._catch_location = value

    @classmethod     
    def output_json(self) -> str:
        data = map_to_json(self)
        return json.dumps(data)
    
    @classmethod 
    def output_xlsx(self) -> str:
        """
        Create an excel spreadsheet and output the contents to an XML string
        """

        # code here

        v = "foobar"
        return v

    @classmethod 
    def save_as_xlsx(self, filename: str):
        pass
        # code here