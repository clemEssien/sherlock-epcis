import datetime
import re


class URI:
    """Provides a class for URI objects as defined in GS1's [TDS1.9, Section 7]

    Attributes:
        uri : str
            Entire uri. Will be present when other attributes cannot be parsed.
        prefix : str
            The first four parts of the URI, denoted by GS1 as the uri prefix.
        scheme : str
            The type of data represented by the URI (SGTIN, SSCC, biztype, etc.).
        value : str
            The data stored by the URI (the actual SGTIN, SSCC, or biztype, etc.).
    """

    def __init__(self, input_str: str):
        """Creates a new URI instance from the given string"""
        self.uri = input_str
        self.prefix = ""
        self.scheme = ""
        self.value = ""
        if re.search("[a-z]+:[a-z]+:[a-z]+:[a-z]+:[a-z0-9.*]+", input_str) is not None:
            uri = input_str.split(":")
            self.prefix = "{}:{}:{}:{}".format(uri[0], uri[1], uri[2], uri[3])
            self.scheme = uri[3]
            self.value = uri[4]

    def __repr__(self) -> str:
        rep = (
            "URI(uri: "
            + self.uri
            + "; prefix: "
            + self.prefix
            + "; scheme: "
            + self.scheme
            + "; value: "
            + self.value
            + ")"
        )
        return rep

    def __str__(self) -> str:
        return self.uri


class QuantityElement:
    """Provides a class for the QuantityElement structure defined in [EPCIS1.2, Section 7.3.3.3]

    Attributes:
        epc_class : URI
            The identifier for the class to which the specified quantity of objects belongs.
        quantity : float
            How many or how much of the specified EPCClass is denoted by this QuantityElement.
        uom : str
            The unit of measure the quantity is to be interpreted as.
    """

    def __init__(self, epc: URI = URI(""), quant: float = -1, unit: str = ""):
        """Creates a new QuantityElement instance"""
        self._epc_class: URI = epc
        self._quantity: float = quant
        self._uom: str = unit

    def __repr__(self) -> str:
        return (
            "QuantityElement("
            + str(self._epc_class)
            + ", "
            + str(self._quantity)
            + ", "
            + self._uom
            + ")"
        )

    @property
    def epc_class(self) -> URI:
        return self._epc_class

    @epc_class.setter
    def epc_class(self, value: URI):
        if isinstance(value, str):
            value = URI(value)
        self._epc_class = value

    @property
    def quantity(self) -> float:
        return self._quantity

    @quantity.setter
    def quantity(self, value: float):
        if isinstance(value, int):
            value = float(value)
        elif isinstance(value, str):
            try:
                value = float(value)
            except:
                pass
        self._quantity = value

    @property
    def uom(self) -> str:
        return self._uom

    @uom.setter
    def uom(self, value: str):
        if not isinstance(value, str):
            try:
                value = str(value)
            except:
                pass
        self._uom = value


class EPCISEvent:
    """Provides a common base type for all EPCIS events [EPCIS1.2, Section 7.4.1]

    Attributes:
        event_time : datetime.datetime
            The date and time that the event occurred.
        event_timezone_offset : datetime.timezone
            The timezone offset in effect at the time and place the event occurred.
    """

    def __init__(self):
        """Creates a new EPCISEvent instance with empty, but type-hinted, attributes"""
        self._event_time = datetime.datetime(1, 1, 1)
        self._event_timezone_offset = datetime.timezone(datetime.timedelta(hours=0))

    def __repr__(self) -> str:
        """EPCISEvent representation"""
        rep = self.__class__.__name__ + "(\n"
        for attr in self.__dict__.keys():
            rep = rep + attr + " : " + str(getattr(self, attr)) + "\n"
        return rep + ")"

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
                offset = value.split(":")
                # computes hours as a float by taking (|hour| + minutes/60) * -1 or +1 depending on the offset's sign
                value = datetime.timezone(
                    datetime.timedelta(
                        hours=(abs(float(offset[0])) + (float(offset[1]) / 60))
                        * (abs(float(offset[0])) / float(offset[0]))
                    )
                )
        self._event_timezone_offset = value


class CommonEvent(EPCISEvent):
    """A class containing attributes not in EPCISEvent, but still shared by most events types.

    Attributes:
        action : str
            How this event relates to the lifecycle of the EPCs named in this event.
        business_step : URI
            The business steps of which this event took place.
        disposition : URI
            The business condition of the objects associated with the EPCs.
        read_point : URI
            The read point at which the event took place.
        business_location : URI
            The business location where the objects associated with the EPCs can be found.
        business_transaction_list : list[dict]
            List of business transactions that define the context of this event.
        source_list : list[dict]
            List of source elements providing context about the originating endpoint of a business
            transfer of which this event is a part.
        destination_list : list[dict]
            List of source elements providing context about the terminating endpoint of a business
            transfer of which this event is a part.
    """

    def __init__(self):
        super().__init__()
        self._action: str = ""
        self._business_step: URI = URI("")
        self._disposition: URI = URI("")
        self._read_point: URI = URI("")
        self._business_location: URI = URI("")
        self._business_transaction_list: list[dict] = []
        self._source_list: list[dict] = []
        self._destination_list: list[dict] = []

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
    def disposition(self) -> URI:
        """disposition"""
        return self._disposition

    @disposition.setter
    def disposition(self, value: URI):
        if isinstance(value, str):
            value = URI(value)
        self._disposition = value

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
    def business_location(self) -> URI:
        """business_location"""
        return self._business_location

    @business_location.setter
    def business_location(self, value: URI):
        if isinstance(value, str):
            value = URI(value)
        self._business_location = value

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


class ObjectEvent(CommonEvent):
    """Provides a class for EPCIS ObjectEvents [EPCIS1.2, Section 7.4.2]

    Attributes:
        epc_list : list[URI]
            List of one or more EPCs naming specific objects to which the event pertained.
        quantity_list : list[QuantityElement]
            List of one or more QuantifyingElements identfiying objects to which the event pertained.
        instance_lot_master_data : dict
            Instance/lot master data that describes the objects created during this event.

    """

    def __init__(self):
        super().__init__()
        self._epc_list: list[URI] = []
        self._quantity_list: list[QuantityElement] = []
        self._instance_lot_master_data: dict = {}

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
    def quantity_list(self) -> list[QuantityElement]:
        """quantity_list"""
        return self._quantity_list

    @quantity_list.setter
    def quantity_list(self, value: list[QuantityElement]):
        if isinstance(value, list):
            new_vals = []
            for val in value:
                if isinstance(val, dict) and "epcClass" in val.keys():
                    qe = QuantityElement()
                    for a_k in [
                        ("epc_class", "epcClass"),
                        ("quantity", "quantity"),
                        ("uom", "uom"),
                    ]:
                        if a_k[1] in val.keys():
                            setattr(qe, a_k[0], val[a_k[1]])
                    new_vals.append(qe)
            if len(new_vals) == len(value):
                value = new_vals
        self._quantity_list = value

    @property
    def instance_lot_master_data(self) -> dict:
        """instance_lot_master_data"""
        return self._instance_lot_master_data

    @instance_lot_master_data.setter
    def instance_lot_master_data(self, value: dict):
        self._instance_lot_master_data = value


class AggregationEvent(CommonEvent):
    """Provides a class for EPCIS AggregationEvents [EPCIS1.2, Section 7.4.3]

    Attributes:
        parent_id : URI
            Identifier off the parent of the association.
        child_epc_list : list[URI]
            List of EPCs of contained objects identified by instance-level identifiers.
        child_quantity_list : list[QuantityElement]
            List of QuantityElements identifying contained objects.
    """

    def __init__(self):
        super().__init__()
        self._parent_id: URI = URI("")
        self._child_epc_list: list[URI] = []
        self._child_quantity_list: list[QuantityElement] = []

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
    def child_quantity_list(self) -> list[QuantityElement]:
        """quantity_list"""
        return self._child_quantity_list

    @child_quantity_list.setter
    def child_quantity_list(self, value: list[QuantityElement]):
        if isinstance(value, list):
            new_vals = []
            for val in value:
                if isinstance(val, dict) and "epcClass" in val.keys():
                    qe = QuantityElement()
                    for a_k in [
                        ("epc_class", "epcClass"),
                        ("quantity", "quantity"),
                        ("uom", "uom"),
                    ]:
                        if a_k[1] in val.keys():
                            setattr(qe, a_k[0], val[a_k[1]])
                    new_vals.append(qe)
            if len(new_vals) == len(value):
                value = new_vals
        self._child_quantity_list = value


class QuantityEvent(EPCISEvent):
    """Provides a class for EPCIS QuantityEvents (DEPRECATED) [EPCIS1.2, Section 7.4.4]

    Attributes:
        epc_class : URI
            Identifier specficying the object class to which the event pertains.
        quantity : int
            Quantity of object within class described by this event.
        business_step : URI
            The business steps of which this event took place.
        disposition : URI
            The business condition of the objects associated with the EPCs.
        read_point : URI
            The read point at which the event took place.
        business_location : URI
            The business location where the objects associated with the EPCs can be found.
        business_transaction_list : list[dict]
            List of business transactions that define the context of this event.
    """

    def __init__(self):
        super().__init__()
        self._epc_class: URI = URI("")
        self._quantity: int = 0
        self._business_step: URI = URI("")
        self._disposition: URI = URI("")
        self._read_point: URI = URI("")
        self._business_location: URI = URI("")
        self._business_transaction_list: list[dict] = []

    @property
    def epc_class(self) -> URI:
        """epc_class"""
        return self._epc_class

    @epc_class.setter
    def epc_class(self, value: URI):
        if isinstance(value, str):
            value = URI(value)
        self._epc_class = value

    @property
    def quantity(self) -> int:
        """quantity"""
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        if isinstance(value, str):
            try:
                value = int(value)
            except:
                pass
        self._quantity = value

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
    def read_point(self) -> URI:
        """read_point"""
        return self._read_point

    @read_point.setter
    def read_point(self, value: URI):
        if isinstance(value, str):
            value = URI(value)
        self._read_point = value

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
    def business_transaction_list(self) -> list[dict]:
        """business_transaction_list"""
        return self._business_transaction_list

    @business_transaction_list.setter
    def business_transaction_list(self, value: list[dict]):
        self._business_transaction_list = value


class TransactionEvent(CommonEvent):
    """Provides a class for EPCIS TransactionEvents [EPCIS1.2, Section 7.4.5]

    Attributes:
        parent_id : URI
            Identifier off the parent of the objects given in epc_list or quantity_list.
        epc_list : list[URI]
            List of one or more EPCs naming specific objects to which the event pertained.
        quantity_list : list[QuantityElement]
            List of one or more QuantifyingElements identfiying objects to which the event pertained.

    """

    def __init__(self):
        super().__init__()
        self._parent_id: URI = URI("")
        self._epc_list: list[URI] = []
        self._quantity_list: list[QuantityElement] = []

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
    def quantity_list(self) -> list[QuantityElement]:
        """quantity_list"""
        return self._quantity_list

    @quantity_list.setter
    def quantity_list(self, value: list[QuantityElement]):
        if isinstance(value, list):
            new_vals = []
            for val in value:
                if isinstance(val, dict) and "epcClass" in val.keys():
                    qe = QuantityElement()
                    for a_k in [
                        ("epc_class", "epcClass"),
                        ("quantity", "quantity"),
                        ("uom", "uom"),
                    ]:
                        if a_k[1] in val.keys():
                            setattr(qe, a_k[0], val[a_k[1]])
                    new_vals.append(qe)
            if len(new_vals) == len(value):
                value = new_vals
        self._quantity_list = value


class TransformationEvent(CommonEvent):
    """Provides a class for EPCIS TransformationEvents [EPCIS1.2, Section 7.4.6]

    Attributes:
        input_epc_list : list[URI]
            List of EPCs identfying objects that were inputs to the transformation.
        input_quantity_list : list[QuantityElement]
            List of QuantityElements identfying objects that were inputs to the transformation.
        output_epc_list : list[URI]
            List of EPCs identfying objects that were outputs from the transformation.
        output_quantity_list : list[QuantityElement]
            List of QuantityElements identfying objects that were outputs from the transformation.
        transformation_id : URI
            Unique identifier linking this event to other TransformationEvents sharing inputs.
        instance_lot_master_data : dict
            Instance/Lot master data that describes the output objects created during this event.

    """

    def __init__(self):
        super().__init__()
        self._input_epc_list: list[URI] = []
        self._input_quantity_list: list[QuantityElement] = []
        self._output_epc_list: list[URI] = []
        self._output_quantity_list: list[QuantityElement] = []
        self._transformation_id: URI = URI("")
        self._instance_lot_master_data: dict = {}

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
    def input_quantity_list(self) -> list[QuantityElement]:
        """input_quantity_list"""
        return self._input_quantity_list

    @input_quantity_list.setter
    def input_quantity_list(self, value: list[QuantityElement]):
        if isinstance(value, list):
            new_vals = []
            for val in value:
                if isinstance(val, dict) and "epcClass" in val.keys():
                    qe = QuantityElement()
                    for a_k in [
                        ("epc_class", "epcClass"),
                        ("quantity", "quantity"),
                        ("uom", "uom"),
                    ]:
                        if a_k[1] in val.keys():
                            setattr(qe, a_k[0], val[a_k[1]])
                    new_vals.append(qe)
            if len(new_vals) == len(value):
                value = new_vals
        self._input_quantity_list = value

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
    def output_quantity_list(self) -> list[QuantityElement]:
        """output_quantity_list"""
        return self._output_quantity_list

    @output_quantity_list.setter
    def output_quantity_list(self, value: list[QuantityElement]):
        if isinstance(value, list):
            new_vals = []
            for val in value:
                if isinstance(val, dict) and "epcClass" in val.keys():
                    qe = QuantityElement()
                    for a_k in [
                        ("epc_class", "epcClass"),
                        ("quantity", "quantity"),
                        ("uom", "uom"),
                    ]:
                        if a_k[1] in val.keys():
                            setattr(qe, a_k[0], val[a_k[1]])
                    new_vals.append(qe)
            if len(new_vals) == len(value):
                value = new_vals
        self._output_quantity_list = value

    @property
    def transformation_id(self) -> URI:
        """transaction_form_id"""
        return self._transformation_id

    @transformation_id.setter
    def transformation_id(self, value: URI):
        if isinstance(value, str):
            value = URI(value)
        self._transformation_id = value

    @property
    def instance_lot_master_data(self) -> dict:
        """instance_lot_master_data"""
        return self._instance_lot_master_data

    @instance_lot_master_data.setter
    def instance_lot_master_data(self, value: dict):
        self._instance_lot_master_data = value


# script showing the different event types
if __name__ == "__main__":
    event_types = {
        "ObjectEvent": ObjectEvent(),
        "AggregationEvent": AggregationEvent(),
        "QuantityEvent": QuantityEvent(),
        "TransactionEvent": TransactionEvent(),
        "TransformationEvent": TransformationEvent(),
    }
    for key in event_types.keys():
        event = event_types[key]
        print(event)

    obj_event = AggregationEvent()

    for attr in obj_event.__dict__.keys():
        attr = attr[1:]
        setattr(obj_event, attr, attr)

    print(obj_event)