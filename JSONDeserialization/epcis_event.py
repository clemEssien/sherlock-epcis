import datetime
import re


class URI():
    """ Provides a class for URI objects

    Attributes:
        prefix : str
            The first four parts of the URI, denoted by GS1 as the uri prefix.
        epc_scheme : str
            The type of data represented by the URI (SGTIN, SSCC, biztype, etc.).
        value : str
            The data stored by the URI (the actual SGTIN, SSCC, or biztype, etc.).
    """
    def __init__(self, input_str:str):
        """Creates a new URI instance from the given string"""
        self.uri = input_str
        if re.search("[a-z]+:[a-z]+:[a-z]+:[a-z]+:[a-z0-9.*]+",input_str) is not None:
            uri = input_str.split(':')
            self.prefix = "{}:{}:{}:{}".format(uri[0],uri[1],uri[2],uri[3])
            self.epc_scheme = uri[3]
            self.value = uri[4]
    def __str__(self):
        return self.uri

#TODO: flesh out event object and replace instances of str where that string represents a URI
class EPCISEvent():
    """ Provides a class for EPCIS Event objects

    Attributes:

    """
    def __init__(self):
        """Creates a new EPCISEvent instance with empty, but type-hinted, attributes"""
        self._event_type: str = ''
        self._event_time = datetime.datetime(1,1,1)
        self._event_timezone_offset = datetime.timezone(datetime.timedelta(hours=0))
        self._epc_list: list[URI] = []
        self._parent_id: URI = ''
        self._child_epc_list: list[URI] = []
        self._input_epc_list: list[URI] = []
        self._output_epc_list: list[URI] = []
        self._xform_id: URI = ''
        self._action: str = ''
        self._business_step: URI = ''
        self._disposition: URI = ''
        self._business_location: URI = ''
        self._read_point: URI = ''
        self._instance_lot_master_data: dict = {}
        self._quantity_list: list[dict] = []
        self._child_quantity_list: list[dict] = []
        self._input_quantity_list: list[dict] = []
        self._output_quantity_list: list[dict] = []
        self._business_transaction_list: list[dict] = []
        self._source_list: list[dict] = []
        self._destination_list: list[dict] = []

        @property
        def event_type(self) -> str:
            """event_type"""
            return self._event_type

        @event_type.setter
        def event_type(self, value: str):
            self._event_type = value

        @property
        def event_time(self) -> datetime.datetime:
            """event_time"""
            return self._event_time

        @event_time.setter
        def event_time(self, value: datetime.datetime):
            self._event_time = value
 
uri1 = URI("abc")
uri2 = URI("urn:epc:class:lgtin:0614141.077777.987")
uri3 = URI("urn:epcglobal:cbv:bizstep:commissioning")

print(uri1.uri)
print(uri1.prefix)

print(uri2.value)
print(uri2.prefix)
print(uri2.epc_scheme)

print(uri3.value)
print(uri3.prefix)
print(uri3.epc_scheme)