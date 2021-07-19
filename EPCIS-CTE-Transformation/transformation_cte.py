from _typeshed import Self
from abc import ABC, abstractclassmethod, abstractmethod
from typing import Type
from JSONDeserialization.epcis_event import QuantityElement, QuantityEvent, URI, CommonEvent, AggregationEvent, EPCISEvent, ObjectEvent, TransactionEvent, TransformationEvent
from cte import CTEBase
import json

class TransformationCTE(CTEBase):
    def __init__(self):
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
        output._location_of_transformation = event._read_point.value
        
        if not isinstance(event, TransformationEvent):
            raise TypeError("Transformation CTE requires TransformationEvent")
        
        transEvent: TransformationEvent = event

        for element in event._input_quantity_list:
            output._quantity_of_input.append(element._quantity)
            output._unit_of_measure.append(element._uom)

        for element in event._output_quantity_list:
            output._quantity_of_output.append(element._quantity)

        for element in event._input_epc_list:
            output._traceability_product.append(element.value)

        for element in event._output_epc_list:
            output._new_traceability_product.append(element.value)

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
    def quantity_of_output(self) -> str:
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
        '''
        Create an excel spreadsheet and output the contents to an XML string
        '''

        # code here
        
        v = "foobar"
        return v
    
    def save_as_xlsx(self, filename: str): 
        pass
        # code here
