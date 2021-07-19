from _typeshed import Self
from abc import ABC, abstractclassmethod, abstractmethod
from typing import Type
from JSONDeserialization.epcis_event import EPCISEvent

class CTEBase(ABC):
    
    @abstractclassmethod
    def new_from_data(cls, data: dict):
        pass

    @abstractclassmethod
    def new_from_epcis(cls, event: EPCISEvent):
        """
        Create a new CTE from an EPCIS event
        """
        pass
    
    @abstractclassmethod
    def new_from_json(cls, json_data: str): 
        pass
    
    @abstractclassmethod
    def new_from_csv(cls, csv_lines: "list[str]"):
        pass

    @abstractclassmethod
    def new_from_excel(cls, excel_data: str):
        pass

    @abstractmethod
    def save_to_excel(self):
        pass
    