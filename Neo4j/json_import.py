import json
import os
from dotenv import load_dotenv
load_dotenv()

import db_connect as db_con
from collections import defaultdict

global conn 
conn = None

def connectdb() -> db_con.Neo4jConnection:
    return db_con.Neo4jConnection(uri=os.getenv("DB_URI"), 
                       user=os.getenv('DB_USER'),              
                       password=os.getenv('DB_PASS'))

def create_relationships(dict_list, node_label):
    global conn
    """method creates relationships between nodes in the json files
       Args: 
            obj: defaultdict(list) of node ids as keys 
            obj: list containing connector ids (i.e. event_ids)
    """
    if not conn: conn = connectdb()
    
    for key, value in dict_list.items():
        for id in value:
            # print(id)
            query = """
                MATCH (a:"""+node_label+"""), (b:"""+node_label+""") 
                WHERE a._id = '"""+key +"""' AND b._id = '"""+id +"""'  
                CREATE (b)-[: next_event]->(a) 
                RETURN a,b 
            """
            conn.query(query, None)


def format_attr_string(attr_str):
    output = attr_str.replace("':", ":").replace(", '",", ").replace("'_id", "_id")
    return output

def delete_nodes_by_label(node_label):
    '''
    This method deletes a node using its _id
    '''
    global conn
    if not conn: conn = connectdb()
    cipher_ql = """ MATCH (n:"""+ node_label + """)
                    DETACH DELETE n
                """
    result = conn.query(cipher_ql,None)
    return result


def create_node_from_json(file, node_label):
    """method takes in a json file and node label 
    Args: 
        file: json file
        str: node label
    """
    global conn    
    if not conn: conn = connectdb()
    
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
            "loc_"+str(count) + " : " + node_label + \
                attr_str + \
            """
        )
        """
        count += 1
        conn.query(query,None)
    create_relationships(relationships,node_label)      