from abc import ABC, abstractclassmethod, abstractmethod
from typing import List, Type
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


class TransformationCTE(CTEBase):
    """
    Provides a class for the Transformation CTE and defines its KDEs

    KDEs:
            Traceability Product : List
            Quantity of Input : List
            Quantity of Output : List
            Location of Transformation : str
            New Traceability Product : List
            Unit of Measure : List
    """

    def __init__(self):
        """Creates new Transformation CTE"""
        self._traceability_product = []
        self._quantity_of_input = []
        self._quantity_of_output = []
        self._location_of_transformation = ""
        self._new_traceability_product = []
        self._unit_of_measure = []

    def new_from_data(cls, data: dict):
        pass

    def new_from_epcis(cls, event: EPCISEvent):
        output = cls()

        # check if TransformationCTE must come from TransformationEvent
        # transEvent: TransformationEvent = event
        if isinstance(event, TransformationEvent):
            output.location_of_transformation = event.read_point.value
            for qe in event.input_quantity_list:
                output.quantity_of_input.append(qe.quantity)
                output.unit_of_measure.append(qe.uom)
            for qe in event.output_quantity_list:
                output.quantity_of_output.append(qe.quantity)
            for epc in event.input_epc_list:
                output.traceability_product.append(epc.value)
            for epc in event.output_epc_list:
                output.new_traceability_product.append(epc.value)
        # transEvent: TransformationEvent = event
        elif isinstance(event, ObjectEvent):
            output.location_of_transformation = event.read_point.value
            for qe in event.quantity_list:
                output.quantity_of_input.append(qe.quantity)
                output.unit_of_measure.append(qe.uom)
            for epc in event.epc_list:
                output.traceability_product.append(epc.value)
        elif isinstance(event, AggregationEvent):
            output.location_of_transformation = event.read_point.value
            for qe in event.child_quantity_list:
                output.quantity_of_input.append(qe.quantity)
                output.unit_of_measure.append(qe.uom)
            for epc in event.child_epc_list:  # check if we should use this or parentID
                output.traceability_product.append(epc.value)
        elif isinstance(event, QuantityEvent):
            output.location_of_transformation = event.read_point.value
            output.quantity_of_input.append(event.quantity)
            output.traceability_product.append(event.epc_class)
        elif isinstance(
            event, TransactionEvent
        ):  # TransactionEvent ... check if a CommonEvent could ever be passed in as the event
            # how to let output know event is a transaction event
            output.location_of_transformation = event.read_point.value
            for qe in event.quantity_list:
                output.quantity_of_input.append(qe.quantity)
                output.unit_of_measure.append(qe.uom)
            for epc in event.epc_list:  # check if we should use this or parentID
                output.traceability_product.append(epc.value)

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
    def traceability_product(self) -> str:
        return self._traceability_product

    @traceability_product.setter
    def traceability_product(self, value: str):
        self._traceability_product = value

    @property
    def quantity_of_input(self) -> str:
        return self._quantity_of_input

    @quantity_of_input.setter
    def quantity_of_input(self, value: str):
        self._quantity_of_input = value

    @property
    def quantity_of_output(self) -> List:
        return self._quantity_of_output

    @quantity_of_output.setter
    def quantity_of_output(self, value: str):
        self._quantity_of_output = value

    @property
    def location_of_transformation(self) -> str:
        return self._location_of_transformation

    @location_of_transformation.setter
    def location_of_transformation(self, value: str):
        self._location_of_transformation = value

    @property
    def new_traceability_product(self) -> str:
        return self._new_traceability_product

    @new_traceability_product.setter
    def new_traceability_product(self, value: str):
        self._new_traceability_product = value

    @property
    def unit_of_measure(self) -> str:
        return self._unit_of_measure

    @unit_of_measure.setter
    def unit_of_measure(self, value: str):
        self._unit_of_measure = value

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
