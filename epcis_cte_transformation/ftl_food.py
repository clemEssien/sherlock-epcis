from tools.serializer import jsonid, map_from_json, map_to_json
import json

from cte import CTEBase
from growing_cte import GrowingCTE
from receiving_cte import ReceivingCTE
from shipping_cte import ShippingCTE
from transformation_cte import TransformationCTE

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
    
class FTLFood:
    
    @classmethod
    def new_from_cte(cls, cte):
        result = cls()
        
        pass
    
    def __init__(self, json = None):
        
        json_dict = None

        if json:
            if isinstance(json, str):
                json_dict = json.loads(json)
            elif isinstance(json, dict):
                json_dict = json
            else:
                raise TypeError
        
        self._id: str = None
        self._product_id: str = None
        self._category_code: str = None
        self._category_name: str = None
        self._brand_name: str = None
        self._commodity: str = None
        self._variety: str = None
        self._product_name: str = None
        self._packaging_size: str = None
        self._packaging_style: str = None

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


