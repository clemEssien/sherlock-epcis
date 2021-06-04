# Author: Ryan Oostland
# Last Update: May 28, 2021
import json

# returns more usable lists of stations, deliveries, and transformations from EPCIS-FCL.json
def deserialize_EPCIS_FCL(input_file):
    stations = []
    deliveries = []
    transformations = []
    with open(input_file) as f:
        epcis_dict = json.load(f)
        # path to Entity Details
        for station in epcis_dict['data']['stations']['data']:
            temp_entity = {}
            for pair in station:
                temp_entity[pair['id']] = pair['value']
            stations.append(temp_entity)
        # path to Product Details
        for delivery in epcis_dict['data']['deliveries']['data']:
            temp_delivery = {}
            for pair in delivery:
                temp_delivery[pair['id']] = pair['value']
            deliveries.append(temp_delivery)
         # path to deliveryRelations (really represent a transformation)
        for transformation in epcis_dict['data']['deliveryRelations']['data']:
            temp_transformation = {}
            for pair in transformation:
                temp_transformation[pair['id']] = pair['value']
            transformations.append(temp_transformation)
    return stations, deliveries, transformations

# currently just prints 
def main():
    stations, deliveries, transformations = deserialize_EPCIS_FCL('EPCIS-FCL.json')
    for station in stations:
        for key, value in station.items():
            print("{} : {}".format(key,value))
        print("")

    for delivery in deliveries:
        for key, value in delivery.items():
            print("{} : {}".format(key,value))
        print("")

    for transformation in transformations:
        for key, value in transformation.items():
            print("{} : {}".format(key,value))
        print("")

if __name__ == '__main__':
    main()