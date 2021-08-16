from tools.serializer import jsonid, map_from_json, map_to_json
import json

from epcis_cte_transformation.cte import CTEBase
from epcis_cte_transformation.creation_cte import CreationCTE
from epcis_cte_transformation.growing_cte import GrowingCTE
from epcis_cte_transformation.receiving_cte import ReceivingCTE
from epcis_cte_transformation.shipping_cte import ShippingCTE
from epcis_cte_transformation.transformation_cte import TransformationCTE


from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.worksheet import Worksheet

# export const ftlFoodsOliveRows = [
# {
# id: 1, //
# productId: "9991002100014", //Growing (traceability_lot_code), Receiving, Shipping, Transformation & Creation (traceability_product)
# categoryCode: "", //
# categoryName: "Olive Oil", //Not Found
# brandName: "Olive Oil Company", //Not Found
# commodity: "Olive Oil", //Not Found
# variety: "", //Not Found
# productName: "", //Not Found
# packagingSize: "100", //Receiving (quantity_received), Shipping & Creation (quantity), Transformation (quantity_of_input)
# packagingStyle: "Palette" //Receiving, Transformation, Creation, Shipping (unit_of_measure)
# },
    
ftl_map = {
    "packagingStyle": [
        {
            "types": [ ReceivingCTE, TransformationCTE, CreationCTE, ShippingCTE ],
            "key": "unit"
        }
    ],
    "packagingSize": [
        {
            "types": [ ReceivingCTE ],
            "key": "quantityReceived"
        },
        {
            "types": [ ShippingCTE, CreationCTE ],
            "key": "quantity"
        },
        {
            "types": [ TransformationCTE ],
            "key": "inputQuantity"
        }
    ],
    "productId": [
        {
            "types": [ GrowingCTE ],
            "key": "traceabilityLotCode"
        },
        {
            "types": [ ReceivingCTE, TransformationCTE ],
            "key": "traceabilityProduct"
        },
        {
            "types": [ ShippingCTE ],
            "key": "traceabilityPid"
        }
    ]
}

def get_map_from_type(key, type):
    if not key in ftl_map:
        return None
    map = ftl_map[key]
    if not map:
        return None
    for cte in map:
        for cte_type in cte["types"]:
            if type == cte_type:
                return cte["key"]
    
    return None
    
class FTLFood:
    
    @classmethod
    def new_from_cte(cls, cte):
        result = cls()
        search = type(cte)
        
        data1 = map_to_json(cte)
        data2 = map_to_json(result)
        
        for key in data2.keys():
            newkey = get_map_from_type(key, search)
            if newkey and newkey in data1:
                data2[key] = data1[newkey]

        map_from_json(data2, result)
        return result
    
    def __init__(self, json = None):
        
        json_dict = None

        if json:
            if isinstance(json, str):
                json_dict = json.loads(json)
            elif isinstance(json, dict):
                json_dict = json
            else:
                raise TypeError
        
        self._id: str = ""
        self._product_id: str = ""
        self._category_code: str = ""
        self._category_name: str = ""
        self._brand_name: str = ""
        self._commodity: str = ""
        self._variety: str = ""
        self._product_name: str = ""
        self._packaging_size: str = ""
        self._packaging_style: str = ""

        if json_dict:
            map_from_json(json_dict, self)

    @property
    @jsonid("id")
    def id(self) -> str:
        return self._id

    @property
    @jsonid("productId")
    def product_id(self) -> str:
        return self._product_id

    @property
    @jsonid("categoryCode")
    def category_code(self) -> str:
        return self._category_code

    @property
    @jsonid("categoryName")
    def category_name(self) -> str:
        return self._category_name

    @property
    @jsonid("brandName")
    def brand_name(self) -> str:
        return self._brand_name

    @property
    @jsonid("commodity")
    def commodity(self) -> str:
        return self._commodity

    @property
    @jsonid("variety")
    def variety(self) -> str:
        return self._variety

    @property
    @jsonid("productName")
    def product_name(self) -> str:
        return self._product_name

    @property
    @jsonid("packagingSize")
    def packaging_size(self) -> str:
        return self._packaging_size

    @property
    @jsonid("packagingStyle")
    def packaging_style(self) -> str:
        return self._packaging_style

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @product_id.setter
    def product_id(self, value: str) -> None:
        self._product_id = value

    @category_code.setter
    def category_code(self, value: str) -> None:
        self._category_code = value

    @category_name.setter
    def category_name(self, value: str) -> None:
        self._category_name = value

    @brand_name.setter
    def brand_name(self, value: str) -> None:
        self._brand_name = value

    @commodity.setter
    def commodity(self, value: str) -> None:
        self._commodity = value

    @variety.setter
    def variety(self, value: str) -> None:
        self._variety = value

    @product_name.setter
    def product_name(self, value: str) -> None:
        self._product_name = value

    @packaging_size.setter
    def packaging_size(self, value: str) -> None:
        self._packaging_size = value

    @packaging_style.setter
    def packaging_style(self, value: str) -> None:
        self._packaging_style = value


    def output_xlsx(self, sheet, row):
        pass
