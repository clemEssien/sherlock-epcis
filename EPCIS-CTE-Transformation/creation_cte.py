from abc import ABC, abstractclassmethod, abstractmethod
from typing import List
from cte import CTEBase
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


class CreationCTE(CTEBase):

    """
    Provides a class for the Creation CTE and defines its KDEs

    KDEs:
            Traceability Product : List
            Creation Completion Date : str
            Location Where Food Was Created : str
            Quantity : List
            Unit of Measure : List
    """

    def __init__(self) -> None:
        """Creates new Shipping CTE"""
        self._traceability_product = []
        self._creation_completion_date = ""
        self._loaction_where_food_was_created = ""
        self._quantity = []
        self._unit_of_measure = []

    def new_from_data(cls, data: dict):
        pass

    def new_from_epcis(cls, event: EPCISEvent):
        # your code here
        output = cls()
        if isinstance(event, ObjectEvent):
            output.creation_completion_date = event.event_time_local
            output.location_where_food_was_created = event.read_point.value
            for epc in event.epc_list:
                output.traceability_product.append(epc.value)
            for qe in event.quantity_list:
                output.quantity.append(qe.quantity)
                output.unit_of_measure.append(qe.uom)
        elif isinstance(event, AggregationEvent):
            output.creation_completion_date = event.event_time_local
            output.location_where_food_was_created = event.read_point.value
            for epc in event.child_epc_list:
                output.traceability_product.append(epc.value)
            for qe in event.child_quantity_list:
                output.quantity.append(qe.quantity)
                output.unit_of_measure.append(qe.uom)
        elif isinstance(event, TransactionEvent):
            output.creation_completion_date = event.event_time_local
            output.location_where_food_was_created = event.read_point.value
            for epc in event.epc_list:
                output.traceability_product.append(epc.value)
            for qe in event.quantity_list:
                output.quantity.append(qe.quantity)
                output.unit_of_measure.append(qe.uom)
        elif isinstance(event, TransformationEvent):
            output.creation_completion_date = event.event_time_local
            output.location_where_food_was_created = event.read_point.value
            for epc in event.input_epc_list:
                output.traceability_product.append(epc.value)
            for qe in event.input_quantity_list:
                output.quantity.append(qe.quantity)
                output.unit_of_measure.append(qe.uom)
        elif isinstance(event, CommonEvent):
            output.creation_completion_date = event.event_time_local
            output.location_where_food_was_created = event.read_point.value
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
    def traceability_product(self) -> List:
        return self._traceability_product

    @traceability_product.setter
    def traceability_product(self, value: List):
        self._traceability_product = value

    @property
    def creation_completion_date(self) -> List:
        return self._creation_completion_date

    @creation_completion_date.setter
    def creation_completion_date(self, value: str):
        self._creation_completion_date = value

    @property
    def location_where_food_was_created(self) -> str:
        return self._location_where_food_was_created

    @location_where_food_was_created.setter
    def location_where_food_was_creatd(self, value: str):
        self._location_where_food_was_created = value

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
