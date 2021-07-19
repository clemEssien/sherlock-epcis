from _typeshed import Self
from JSONDeserialization import epcis_event


class TransformationCTE:
    def __init__(self):
        self._traceability_product = ""
        self._quantity_of_input = 0.0
        self._quantity_of_output = 0.0
        self._location_of_transformation = ""
        self._new_traceability_product = ""
        self._unit_of_measure = ""

    @property
    def traceability_product(self) -> str:
        return self._traceability_product

    @traceability_product.setter
    def traceability_product(self, value: str):
        self._traceability_product = value

    @property
    def quantity_of_input(self) -> str:
        return self._quantity_of_input

    @quantity_of_input.setter
    def quantity_of_input(self, value: str):
        self._quantity_of_input = value

    @property
    def quantity_of_output(self) -> str:
        return self._quantity_of_output

    @quantity_of_output.setter
    def quantity_of_output(self, value: str):
        self._quantity_of_output = value

    @property
    def location_of_transformation(self) -> str:
        return self._location_of_transformation

    @location_of_transformation.setter
    def location_of_transformation(self, value: str):
        self._location_of_transformation = value

    @property
    def new_traceability_product(self) -> str:
        return self._new_traceability_product

    @new_traceability_product.setter
    def new_traceability_product(self, value: str):
        self._new_traceability_product = value

    @property
    def unit_of_measure(self) -> str:
        return self._unit_of_measure

    @unit_of_measure.setter
    def unit_of_measure(self, value: str):
        self._unit_of_measure = value

    def map_epcis_to_kde(self, event: epcis_event.TransformationEvent):
        self._location_of_transformation = event._read_point.value
        for element in event._input_quantity_list:
            self._quantity_of_input += element._quantity
            self._unit_of_measure = element._uom

        for element in event._output_quantity_list:
            self._quantity_of_output += element._quantity

        for element in event._input_epc_list:
            self._traceability_product = element.value
            break

        for element in event._output_epc_list:
            self.traceability_product = element.value
            break
