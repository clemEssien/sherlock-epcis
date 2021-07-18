import json
import os
import db_connect as db_con
from collections import defaultdict

conn = db_con.Neo4jConnection(uri="bolt://localhost:7687", 
                       user="neo4j",              
                       password=os.environ['NEO4J_PASSWORD'])

def create_relationships(dict_list):
    for key, value in dict_list.items():
        for id in value:
            print(id)
            query = """
                MATCH (a:Pdt_Location), (b:Pdt_Location) 
                WHERE a.id = '"""+key +"""' AND b.id = '"""+id +"""'  
                CREATE (a)-[: next]->(b) 
                RETURN a,b 
            """
            
            response = conn.query(query, None)
            print(response)
        print("**************")


def format_attr_string(attr_str):
    output = attr_str.replace("':", ":").replace(", '",", ").replace("'_id", "id")
    return output

def create_node_from_json(file):
    exclude_list = ["flowid","connections", "objects", "association" ]
    relationships = defaultdict(list)

    with open(file) as f:
        json_file = json.load(f)
    key_values = {}
    for record in json_file["data"]["events"]:
        id = ""
        query = ""
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
            key_values["name"] = record['location']
            attr_str = format_attr_string(key_values.__str__())
            query = """ 
            CREATE (""" + \
                "pdt_evt" + ":" + "Pdt_Location" + \
                attr_str + \
                """
            )
            """
            response = conn.query(query,None)
            print(response)
    create_relationships(relationships)        
    

create_node_from_json("neo4j/json_files/9991002100014-OL001.json")
create_node_from_json("neo4j/json_files/9991001100015-TO001.json")
create_node_from_json("neo4j/json_files/9991000100016-CT001.json")
create_node_from_json("neo4j/json_files/9991000100030-BP001.json")
create_node_from_json("neo4j/json_files/9991002100014-OL001.json")

