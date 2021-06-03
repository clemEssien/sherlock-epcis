import datetime
import re


class URI():
    """ Provides a class for URI objects as defined in GS1's [TDS1.9, Section 6]

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
    def __repr__(self) -> str:
        rep = 'URI(' + self.uri + ' = ' + self.prefix + ':' + self.value + ')'
        return rep


#TODO: flesh out event object
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
        """event_timezone_offset"""
        return self._event_timezone_offset

    @event_timezone_offset.setter
    def event_timezone_offset(self, value: datetime.timezone):
        if isinstance(value, str):
            if re.search("[+-][0-1][0-9]:[0-5][0-9]", value) is not None:
                offset = value.split(':')
                # computes hours as a float by taking (|hour| + minutes/60) * -1 or +1 depending on the offset's sign
                value = datetime.timezone(datetime.timedelta(hours=
                    (abs(float(offset[0]))+(float(offset[1])/60))*(abs(float(offset[0]))/float(offset[0]))))
        self._event_timezone_offset = value

    @property
    def epc_list(self) -> list[URI]:
        """epc_list"""
        return self._epc_list

    @epc_list.setter
    def epc_list(self, value: list[URI]):
        if isinstance(value, list):
            new_values = []
            for epc in value:
                if isinstance(epc, str):
                    new_values.append(URI(epc))
            if len(new_values) == len(value):
                value = new_values
        self._epc_list = value

    @property
    def parent_id(self) -> URI:
        """parent_id"""
        return self._parent_id

    @parent_id.setter
    def parent_id(self, value: URI):
        if isinstance(value, str):
            value = URI(value)
        self._parent_id = value

    @property
    def child_epc_list(self) -> list[URI]:
        """child_epc_list"""
        return self._child_epc_list

    @child_epc_list.setter
    def child_epc_list(self, value: list[URI]):
        if isinstance(value, list):
            new_values = []
            for epc in value:
                if isinstance(epc, str):
                    new_values.append(URI(epc))
            if len(new_values) == len(value):
                value = new_values
        self._child_epc_list = value

    @property
    def output_epc_list(self) -> list[URI]:
        """output_epc_list"""
        return self._output_epc_list

    @output_epc_list.setter
    def output_epc_list(self, value: list[URI]):
        if isinstance(value, list):
            new_values = []
            for epc in value:
                if isinstance(epc, str):
                    new_values.append(URI(epc))
            if len(new_values) == len(value):
                value = new_values
        self._output_epc_list = value

    @property
    def input_epc_list(self) -> list[URI]:
        """input_epc_list"""
        return self._input_epc_list

    @input_epc_list.setter
    def input_epc_list(self, value):
        if isinstance(value, list):
            new_values = []
            for epc in value:
                if isinstance(epc, str):
                    new_values.append(URI(epc))
            if len(new_values) == len(value):
                value = new_values
        self._input_epc_list = value

    @property
    def xform_id(self) -> URI:
        """transaction_form_id"""
        return self._xform_id

    @xform_id.setter
    def xform_id(self, value: URI):
        if isinstance(value, str):
            value = URI(value)
        self._xform_id = value

    @property
    def action(self) -> str:
        """action"""
        return self._action

    @action.setter
    def action(self, value: str):
        self._action = value

    @property
    def business_step(self) -> URI:
        """business_step"""
        return self._business_step

    @business_step.setter
    def business_step(self, value: URI):
        if isinstance(value, str):
            value = URI(value)

    @property
    def business_step(self) -> URI:
        """business_step"""
        return self._business_step

    @business_step.setter
    def business_step(self, value: URI):
        if isinstance(value, str):
            value = URI(value)
        self._business_step = value

    @property
    def disposition(self) -> URI:
        """disposition"""
        return self._disposition

    @disposition.setter
    def disposition(self, value: URI):
        if isinstance(value, str):
            value = URI(value)
        self._disposition = value

    @property
    def business_location(self) -> URI:
        """business_location"""
        return self._business_location

    @business_location.setter
    def business_location(self, value: URI):
        if isinstance(value, str):
            value = URI(value)
        self._business_location = value

    @property
    def read_point(self) -> URI:
        """read_point"""
        return self._read_point

    @read_point.setter
    def read_point(self, value: URI):
        if isinstance(value, str):
            value = URI(value)
        self._read_point = value

    @property
    def instance_lot_master_data(self) -> dict:
        """instance_lot_master_data"""
        return self._instance_lot_master_data
    
    @instance_lot_master_data.setter
    def instance_lot_master_data(self, value: dict):
        self._instance_lot_master_data = value

    @property
    def quantity_list(self) -> list[dict]:
        """quantity_list"""
        return self._quantity_list

    @quantity_list.setter
    def quantity_list(self, value: list[dict]):
        self._quantity_list = value

    @property
    def child_quantity_list(self) -> list[dict]:
        """child_quantity_list"""
        return self._child_quantity_list

    @child_quantity_list.setter
    def child_quantity_list(self, value: list[dict]):
        self._child_quantity_list = value

    @property
    def input_quantity_list(self) -> list[dict]:
        """input_quantity_list"""
        return self._input_quantity_list

    @input_quantity_list.setter
    def input_quantity_list(self, value: list[dict]):
        self._input_quantity_list = value

    @property
    def output_quantity_list(self) -> list[dict]:
        """output_quantity_list"""
        return self._output_quantity_list

    @output_quantity_list.setter
    def output_quantity_list(self, value: list[dict]):
        self._output_quantity_list = value

    @property
    def business_transaction_list(self) -> list[dict]:
        """business_transaction_list"""
        return self._business_transaction_list

    @business_transaction_list.setter
    def business_transaction_list(self, value: list[dict]):
        self._business_transaction_list = value

    @property
    def source_list(self) -> list[dict]:
        """source_list"""
        return self._source_list

    @source_list.setter
    def source_list(self, value: list[dict]):
        self._source_list = value

    @property
    def destination_list(self) -> list[dict]:
        """destination_list"""
        return self._destination_list

    @destination_list.setter
    def destination_list(self, value: list[dict]):
        self._destination_list = value

event = EPCISEvent()
event.business_location = "urn:epc:id:sgln:0614141.00888.0"
print(event.business_location)

