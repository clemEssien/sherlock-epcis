import datetime
import re


class URI():
    """ Provides a class for URI objects

    Attributes:
        uri : str
            Entire uri. Will be present when other attributes cannot be parsed.
        prefix : str
            The first four parts of the URI, denoted by GS1 as the uri prefix.
        epc_scheme : str
            The type of data represented by the URI (SGTIN, SSCC, biztype, etc.).
        value : str
            The data stored by the URI (the actual SGTIN, SSCC, or biztype, etc.).
    """
    def __init__(self, input_str: str):
        """Creates a new URI instance from the given string"""
        self.uri = input_str
        self.prefix = ''
        self.epc_scheme = ''
        self.value = ''
        if re.search("[a-z]+:[a-z]+:[a-z]+:[a-z]+:[a-z0-9.*]+",input_str) is not None:
            uri = input_str.split(':')
            self.prefix = "{}:{}:{}:{}".format(uri[0],uri[1],uri[2],uri[3])
            self.epc_scheme = uri[3]
            self.value = uri[4]


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
        self._parent_id: URI = URI('')
        self._child_epc_list: list[URI] = []
        self._input_epc_list: list[URI] = []
        self._output_epc_list: list[URI] = []
        self._xform_id: URI = URI('')
        self._action: str = ''
        self._business_step: URI = URI('')
        self._disposition: URI = URI('')
        self._business_location: URI = URI('')
        self._read_point: URI = URI('')
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
        if isinstance(value, str):
            try:
                value = datetime.datetime.fromisoformat(value)
            except:
                pass
        self._event_time = value

    @property
    def event_timezone_offset(self) -> datetime.timezone:
        return self._event_timezone_offset

    @event_timezone_offset.setter
    def event_timezone_offset(self, value: datetime.timezone):
        if re.search("[+-][0-1][0-9]:[0-5][0-9]", value) is not None:
            offset = value.split(':')
            # computes hours as a float by taking (|hour| + minutes/60) * -1 or +1 depending on the original sign of the offset
            value = datetime.timezone(datetime.timedelta(hours=
                (abs(float(offset[0]))+(float(offset[1])/60)*(abs(float(offset[0]))/float(offset[0])))))
        self._event_timezone_offset = value

event = EPCISEvent()
event.event_timezone_offset = "+02:00"
print(event.event_timezone_offset)