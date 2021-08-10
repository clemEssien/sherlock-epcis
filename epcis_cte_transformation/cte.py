from abc import ABC, abstractclassmethod, abstractmethod
from typing import Type
import os, sys
from urllib.parse import SplitResultBytes

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

def split_on(input: dict, key: str) -> "list[dict]":
    arrlen = len(input[key])
    output = []

    for idx in range(0, arrlen):
        newobj = input.copy()
        newobj[key] = input[key][idx]
        output.append(newobj)
        
    return output

def split_results(input: dict) -> "list[dict]":
    arrlist = []
    
    for key in input.keys():
        if isinstance(input[key], list):
            arrlist.append(key)
    
    work = []
    output = [ input ]

    for key in arrlist:
        for item in output:
            splitres = split_on(item, key)
            for r in splitres: work.append(r)
            
        output = work
        work = []
            
    return output