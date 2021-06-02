import datetime

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
        uri = input_str.split(':')
        self._prefix = "{}:{}:{}:{}".format(uri[0],uri[1],uri[2],uri[3])
        self._epc_scheme = uri[3]
        self._value = uri[4]

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
        self._epc_list: list[str] = []
        self._parent_id: str = ''
        self._child_epc_list: list[str] = []
        self._input_epc_list: list[str] = []
        self._output_epc_list: list[str] = []
        self._xform_id: str = ''
        self._action: str = ''
        self._business_step: str = ''
        self._disposition: str = ''
        self._business_location: str = ''
        self._read_point: str = ''
        self._instance_lot_master_data: dict = {}
        self._quantity_list: list[dict] = []
        self._child_quantity_list: list[dict] = []
        self._input_quantity_list: list[dict] = []
        self._output_quantity_list: list[dict] = []
        self._business_transaction_list: list[dict] = []
        self._source_list: list[dict] = []
        self._destination_list: list[dict] = []




