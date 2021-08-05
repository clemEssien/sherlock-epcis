from abc import ABC, abstractclassmethod, abstractmethod
from typing import List, Type
import os, sys
import datetime
import json

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

from openpyxl import Workbook, load_workbook
from tools.serializer import JSONValueProvider, jsonid, map_from_json, map_to_json


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
        elif isinstance(event, TransactionEvent):
            output.location_of_transformation = event.read_point.value
            for qe in event.quantity_list:
                output.quantity_of_input.append(qe.quantity)
                output.unit_of_measure.append(qe.uom)
            for epc in event.epc_list:  # check if we should use this or parentID
                output.traceability_product.append(epc.value)
        elif isinstance(event, CommonEvent):
            output.location_of_transformation = event.read_point.value
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

    def output_json(self) -> str:
        pass

    def output_xlsx(self) -> str:
        """
        Create an excel spreadsheet
        """

        workbook = Workbook()
        sheet = workbook.active
        filename = "transformation_cte"

        kde_ids = [
            "Traceability Product",
            "Quantity of Input",
            "Quantity of Output",
            "Location of Transformation",
            "New Traceability Product",
            "Unit of Measure",
        ]
        traceability_product_str = ", ".join(self.traceability_product)
        quantity_of_input_str = ", ".join(self.quantity_of_input)
        quantity_of_output_str = ", ".join(self.quantity_of_output)
        new_traceability_product_str = ", ".join(self.new_traceability_product)
        uom_str = ", ".join(self.unit_of_measure)
        kde_values = [
            traceability_product_str,
            quantity_of_input_str,
            quantity_of_output_str,
            self.location_of_transformation,
            new_traceability_product_str,
            uom_str,
        ]

        for i in range(1, 7):
            cell = sheet.cell(row=1, column=i)
            cell.value = kde_ids[i - 1]

        for i in range(1, 7):
            cell = sheet.cell(row=2, column=i)
            cell.value = kde_values[i - 1]
        # /var/src/documents/<companyid>/<userid>/<cte types>/<name/id>_<timestamp>.xlsx
        # Unknown: companyID, userID, CTETypes, name/id
        # workbook.save('/var/src/documents/' + filename + " " + datetime.datetime.now + '.xlsx')
        workbook.save(filename + ".xlsx")
        return filename

    def save_as_xlsx(self, filename: str):
        pass
        # code here
