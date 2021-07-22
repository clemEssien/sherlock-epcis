import json
import os
import db_connect as db_con
from collections import defaultdict

def create_relationships(dict_list, product, conn):
    for key, value in dict_list.items():
        for id in value:
            print(id)
            query = """
                MATCH (a:"""+product+"""), (b:"""+product+""") 
                WHERE a._id = '"""+key +"""' AND b._id = '"""+id +"""'  
                CREATE (b)-[: next_event]->(a) 
                RETURN a,b 
            """
            
            response = conn.query(query, None)
            print(response)


def format_attr_string(attr_str):
    output = attr_str.replace("':", ":").replace(", '",", ").replace("'_id", "_id")
    return output

def create_node_from_json(file, product):
    conn = db_con.Neo4jConnection(uri="bolt://localhost:7687", 
                       user="neo4j",              
                       password=os.environ['NEO4J_PASSWORD'])
    lst = []
    exclude_list = ["flowid","connections", "objects", "association" ]
    relationships = defaultdict(list)

    with open(file) as f:
        json_file = json.load(f)
    key_values = {}
    count = 1
    for record in json_file["data"]["events"]:
        id = ""
        for key, value in record.items():
            if key == "_id":
                id = record[key]
            if key not in exclude_list:
                key_values[key] = value
            if key == "objects":
               objects = record["objects"]
               objects_len = len(record["objects"])
               for i in range(objects_len):
                for key, value in objects[i].items():
                    key_values[key] = value
            if key == "connections":
                connections = record["connections"]
                for event_id in connections:
                    relationships[id].append(event_id["event_id"])
            key_values["name"] = record['location'] + ' \n [' + record['type']+']'
            attr_str = format_attr_string(key_values.__str__())
        query = """ 
        CREATE (""" + \
            "loc_"+str(count) + " : " + product + \
                attr_str + \
            """
        )
        """
        count += 1
        response = conn.query(query,None)
    create_relationships(relationships,product, conn)        
    
create_node_from_json("neo4j/json_files/9991000100016-CT001.json", "cut_tomato")
create_node_from_json("neo4j/json_files/9991000100023-PS001.json", "ps")
create_node_from_json("neo4j/json_files/9991000100030-BP001.json", "bp")
create_node_from_json("neo4j/json_files/9991001100015-TO001.json", "tomato")
create_node_from_json("neo4j/json_files/9991002100014-OL001.json", "olive")

