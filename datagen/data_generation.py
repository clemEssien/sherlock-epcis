from uuid import UUID
import json
from os.path import join, split
import datetime
import xmltodict
import os
import sys

report_mode = False

if len(sys.argv) >= 2:
    if "--report" in sys.argv:
        report_mode = True

data = {}
text = ""

_f = os.listdir("./data")
files = []

for fp in _f:
    if ".xml" in fp:
        files.append(fp)

files.sort()
nodes = []

for file in files:
    fullpath = join("./data", file)
    
    with open(fullpath) as f:
        text = f.read()
    
    dr = xmltodict.parse(text)
    nodes.append(dr)

# with open("neo4j/json_files/9991000100023-PS001.json") as f:
#     text = f.read()

# data = json.loads(text)

# nodes: list = data["data"]["events"]

a = []

c = len(nodes)

def flatten_data(node, path = None):
    d = []
    if isinstance(node, dict):
        for key in node.keys():
            v = flatten_data(node[key], join(path, key))
            if isinstance(v, list):
                for r in v:
                    d.append(r)    
            else:
                d.append(v)
                
    elif isinstance(node, list):
        for i in range(0, len(node)):
            v = flatten_data(node[i], join(path, str(i)))
            if v and isinstance(v, list) and len(v):
                for r in v:
                    d.append(r)    


        pass    
    
    else:
        return {
            "key": path,
            "data": node
        }

    return d    


f = []

for x in range(0, len(nodes)):
    f.append(flatten_data(nodes[x], "node" + str(x)))

values = {}

for x in range(0, len(f)):
    node1 = f[x]
    
    for y in range(0, len(f)):
        if (x == y): continue
        node2 = f[y]
        
        for pieces1 in node1:
            
            for pieces2 in node2:
                
                if (pieces1["data"] == pieces2["data"]):
                    n = pieces1["data"]
                    key = str(pieces1["data"])
                    # if not isinstance(n, int):
                    #     try:
                    #         n = int(key)
                    #     except:
                    #         pass
                        
                    # if isinstance(n, int):
                    #     if n < 1000000:
                    #         continue
                    # else:
                    #     try:
                    #         u = UUID(key)
                    #     except:
                    #         pass
                    #         continue
                    if not ("gtin" in key or "gtin" in pieces1["key"]) and not ("gln" in key or "gln" in pieces1["key"]):
                            continue

                    if not key in values.keys():
                        values[key] = []
                        
                    if not pieces1["key"] in values[key]:
                            values[key].append(pieces1["key"])
                            values[key].append(pieces1["key"])
                    
        
        

if not report_mode:
    print(json.dumps(values))
else:
    props = {}
    
    for key in values.keys():
        for path in values[key]:
            parts = split(path)
            for pc in range(0, len(parts)):
                path = join(parts[1:])
            
            
    
    