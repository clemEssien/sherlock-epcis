# Author: Kevin Zong
# Last Modified: June 19th, 2021
# Class representing Receiving CTE/KDE data

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
import datetime


class ReceivingCTE:
    """
    Provides a class for the Receiving CTE and defines its KDEs

    KDEs:

            Traceability Lot Code : List
            Growing Coordinates : str
    """

    def __init__(self):
        self._traceability_lot_code = []
        self._growing_location = ""

    def new_from_data(cls, data: dict):
        pass

    def new_from_epcis(cls, event: EPCISEvent):
        output = cls()

        if(issubclass(type(event), CommonEvent)):
            output.growing_location = event.business_location.value

        if isinstance(event, ObjectEvent):
            for epc in event.epc_list:
                output.traceability_lot_code.append(epc.value)
        
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
    def traceability_lot_code(self) -> str:
        return self._traceability_lot_code

    @traceability_lot_code.setter
    def traceability_lot_code(self, value: str):
        self._traceability_lot_code = value

    @property
    def growing_location(self) -> str:
        return self._growing_location

    @growing_location.setter
    def growing_location(self, value: str):
        self._growing_location = value  

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