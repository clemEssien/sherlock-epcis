from abc import ABC, abstractclassmethod, abstractmethod
from typing import Type
import os, sys

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from abc import ABC, abstractclassmethod, abstractmethod
from typing import Type
from JSONDeserialization.epcis_event import EPCISEvent


class CTEBase(ABC):
    @abstractclassmethod
    def new_from_data(cls, data: dict):
        """
        Create a new CTE from a dictionary
        """
        pass

    @abstractclassmethod
    def new_from_epcis(cls, event: EPCISEvent):
        """
        Create a new CTE from an EPCIS event
        """
        pass

    @abstractclassmethod
    def new_from_json(cls, json_data: str):
        """
        Create a new CTE from JSON file
        """
        pass

    @abstractclassmethod
    def new_from_csv(cls, csv_lines: "list[str]"):
        """
        Create a new CTE from CSV file
        """
        pass

    @abstractclassmethod
    def new_from_excel(cls, excel_data: str):
        """
        Create a new CTE from Excel file
        """
        pass

    @abstractmethod
    def save_to_excel(self):
        pass

    @abstractmethod
    def output_json(self):
        pass

    @abstractmethod
    def output_xlsx(self) -> str:
        pass

    @abstractmethod
    def save_as_xlsx(self, filename: str):
        pass
    def export_to_json(self):
        pass
