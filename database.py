from abc import ABC, abstractmethod

class DatabaseConnectorBase(ABC):
    def __init__(self, conn_str: str):
        self._conn_str = conn_str
        self._connected = False
        pass
    
    @property
    def conn_str(self) -> str:
        return self._conn_str
   
    @property
    def connected(self) -> bool:
        return self._connected
    
    @abstractmethod
    def connect(self) -> bool:
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        pass
    
    @abstractmethod
    def query(self, *args, **kwargs):
        pass
    
    @abstractmethod
    def create_record(self, data, *args, **kwargs):
        pass
    
    @abstractmethod
    def delete_one(self, where, *args, **kwargs):
        pass
    
    @abstractmethod
    def delete_many(self, where, *args, **kwargs):
        pass
    
    @abstractmethod
    def find_one(self, where, *args, **kwargs):
        pass
    
    @abstractmethod
    def find_many(self, where, *args, **kwargs):
        pass
    
    @abstractmethod
    def update_one(self, where, data, *args, **kwargs):
        pass

    @abstractmethod
    def update_many(self, where, data, *args, **kwargs):
        pass

    