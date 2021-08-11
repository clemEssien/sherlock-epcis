
from tools.serializer import map_to_json
import json
from epcis_cte_transformation.location_master import LocationMaster


if __name__ == "__main__":
    
    test = LocationMaster()
    
    test.product_id = "AB1234"
    test.product_name = "Tomatoes"
    test.packaging_size = "100 kg"
    test.packaging_style = "Shrink wrapped"
    test.brand_name = "Ella's Famous Tomatoes"
    test.commodity = "Whole Tomatoes"
    test.variety = "Californian"
    test_dict = map_to_json(test)
    
    print(json.dumps(test_dict))
    
