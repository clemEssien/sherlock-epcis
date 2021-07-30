from datetime import datetime
from uuid import UUID, uuid4
from serializer import JSONValueProvider, jsonid, map_from_json, map_to_json 
import json

class CustomClass(JSONValueProvider):    
    def __init__(self, carrots=0, onions=0, radishes=0) -> None:
        super().__init__()
        
        self._carrots: int = carrots
        self._onions: int = onions
        self._radishes: int = radishes
    
    def getvalue(self):
        return [ self._carrots, self._onions, self._radishes ]
    
    def newfromvalue(cls, value):
        newinst = cls()
        newinst.carrots = value[0]
        newinst.onions = value[1]
        newinst.radishes = value[2]
        return newinst
    
    @property
    def carrots(self) -> int:
        return self._carrots
    
    @carrots.setter
    def carrots(self, value: int) -> None:
        self._carrots = value
        
    @property
    def onions(self) -> int:
        return self._onions

    @onions.setter
    def onions(self, value: int) -> None:
        self._onions = value
    
    @property
    def radishes(self) -> int:
        return self._radishes
    
    @radishes.setter
    def radishes(self, value: int) -> None:
        self._radishes = value
    
    
    

class ExampleClass:

    def __init__(self, name: str, carrots: int, onions: int, radishes: int, comments: str = "") -> None:
        self._name: str = name
        self._user_id: UUID = uuid4()
        self._extra_comments: str = comments
        self._date: datetime = datetime.utcnow()
        self._custom: CustomClass = CustomClass(carrots, onions, radishes)

        pass
    
    @property
    @jsonid("name")
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        self._name = value
        
    @property
    @jsonid("userId")
    def user_id(self) -> UUID:
        return self._user_id
    
    @user_id.setter
    def user_id(self, value: UUID) -> None:
        self._user_id = value
        
    @property
    @jsonid("extraComments")
    def extra_comments(self) -> str:
        return self._extra_comments
    
    @extra_comments.setter
    def extra_comments(self, value: str) -> None:
        self._extra_comments = value
    

    @property
    @jsonid("date")
    def date(self) -> datetime:
        return self._date
    
    @date.setter
    def date(self, value: datetime) -> None:
        self._date = value
        
    @property
    @jsonid("custom")
    def custom(self) -> CustomClass:
        return self._custom    
    
    @custom.setter
    def custom(self, value: CustomClass) -> None:
        self._custom = value
    
    
    
if __name__ == "__main__":
    example = ExampleClass("Nathan", 4, 3, 9, "Extra comments go here")
    
    data = map_to_json(example)
    serialized = json.dumps(data)
    
    print("JSON Data:")
    print(serialized)
    print("")
    print("Changing custom data")
    
    data["custom"] = [ 15, 19, 22 ]
    data["extraComments"] = "The comments have been changed"
    
    print("")
    print("Mapping back from JSON:")
    map_from_json(data, example)

    print("")
    print("Carrots: " + str(example.custom.carrots))
    print("Onions: " + str(example.custom.onions))
    print("Carrots: " + str(example.custom.radishes))
    print("")
    
    data = map_to_json(example)
    serialized = json.dumps(data)
    
    print("New JSON Data:")
    print(serialized)
    print("")
    
    
    
    
    