from cte import CTEBase
from JSONDeserialization.epcis_event import QuantityElement, QuantityEvent, URI, CommonEvent, AggregationEvent, EPCISEvent, ObjectEvent, TransactionEvent, TransformationEvent

class ReceivingCTE(CTEBase):
    def __init__(self) -> None:
        pass
    
    def new_from_data(cls, data: dict):
        pass

    def new_from_epcis(cls, event: EPCISEvent):
        # your code here
        pass
    
    def new_from_json(cls, json_data: str): 
        pass
    
    def new_from_csv(cls, csv_lines: "list[str]"):
        pass
    
    def new_from_excel(cls, excel_data: str):
        pass

    def save_to_excel(self):
        pass


