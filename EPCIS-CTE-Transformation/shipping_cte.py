from abc import ABC, abstractclassmethod, abstractmethod
from typing import List
from cte import CTEBase
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


class ShippingCTE(CTEBase):

    """
    Provides a class for the Shipping CTE and defines its KDEs

    KDEs:
            Traceability Lot Code : List
            Entry Number : str
            Quantity : List
            Unit of Measure : List
            Traceability Product : List
            Location of Traceability Lot Code Generator : str
            Location of Recipient : str
            Location of Source of Shipment : str
    """

    def __init__(self) -> None:
        """Creates new Shipping CTE"""
        self._traceability_lot_code = []
        self._entry_number = ""
        self._quantity = []
        self._unit_of_measure = []
        self._traceability_product = []
        self._location_of_traceability_lot_code_generator = ""
        self._location_of_recipient = ""
        self._location_of_source_of_shipment = ""

    def new_from_data(cls, data: dict):
        pass

    def new_from_epcis(cls, event: EPCISEvent):
        # your code here
        output = cls()
        if isinstance(event, ObjectEvent):
            output.location_of_recipient = event.business_location.value
            output.location_of_source_of_shipment = event.read_point.value
            for qe in event.quantity_list:
                output.quantity.append(qe.quantity)
                output.unit_of_measure.append(qe.uom)
                output.traceability_lot_code.append(qe.epc_class.value)
            for epc in event.epc_list:  # check what should be traceability lot code
                output.traceability_product.append(epc.value)
        elif isinstance(event, AggregationEvent):
            output.location_of_recipient = event.business_location.value
            output.location_of_source_of_shipment = event.read_point.value
            for qe in event.child_quantity_list:
                output.quantity.append(qe.quantity)
                output.unit_of_measure.append(qe.uom)
                output.traceability_lot_code.append(qe.epc_class.value)
            for epc in event.child_epc_list:
                output.traceability_product.append(epc.value)
        elif isinstance(event, TransactionEvent):
            output.location_of_recipient = event.business_location.value
            output.location_of_source_of_shipment = event.read_point.value
            for qe in event.quantity_list:
                output.quantity.append(qe.quantity)
                output.unit_of_measure.append(qe.uom)
                output.traceability_lot_code.append(qe.epc_class.value)
            for epc in event.epc_list:
                output.traceability_product.append(epc.value)
        elif isinstance(event, TransformationEvent):
            output.location_of_recipient = event.business_location.value
            output.location_of_source_of_shipment = event.read_point.value
            for qe in event.input_quantity_list:
                output.quantity.append(qe.quantity)
                output.unit_of_measure.append(qe.uom)
                output.traceability_lot_code.append(qe.epc_class.value)
            for epc in event.input_epc_list:
                output.traceability_product.append(epc.value)
        elif isinstance(event, CommonEvent):
            output.location_of_recipient = event.business_location.value
            output.location_of_source_of_shipment = event.read_point.value

        return output

    def new_from_json(cls, json_data: str):
        pass

    def new_from_csv(cls, csv_lines: "list[str]"):
        pass

    def new_from_excel(cls, excel_data: str):
        pass

    def save_to_excel(self):
        pass

    @property
    def traceability_lot_code(self) -> str:
        return self._traceability_lot_code

    @traceability_lot_code.setter
    def traceability_lot_code(self, value: str):
        self._traceability_lot_code = value

    @property
    def entry_number(self) -> str:
        return self._entry_number

    @entry_number.setter
    def entry_number(self, value: str):
        self._entry_number = value

    @property
    def quantity(self) -> List:
        return self._quantity

    @quantity.setter
    def quantity(self, value: List):
        self._quantity = value

    @property
    def unit_of_measure(self) -> List:
        return self._unit_of_measure

    @unit_of_measure.setter
    def unit_of_measure(self, value: List):
        self._unit_of_measure = value

    @property
    def traceability_product(self) -> List:
        return self._traceability_product

    @traceability_product.setter
    def traceability_product(self, value: List):
        self._traceability_product = value

    @property
    def location_of_traceability_lot_code_generator(self) -> str:
        return self._location_of_traceability_lot_code_generator

    @location_of_traceability_lot_code_generator.setter
    def location_of_traceability_lot_code_generator(self, value: str):
        self._location_of_traceability_lot_code_generator = value

    @property
    def location_of_recipient(self) -> str:
        return self._location_of_recipient

    @location_of_recipient.setter
    def location_of_recipient(self, value: str):
        self._location_of_recipient = value

    @property
    def location_of_source_of_shipment(self) -> str:
        return self._location_of_source_of_shipment

    @location_of_source_of_shipment.setter
    def location_of_source_of_shipment(self, value: str):
        self._location_of_source_of_shipment = value

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
