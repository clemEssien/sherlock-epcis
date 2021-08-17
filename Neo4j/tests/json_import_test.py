import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import json_import as js

def test_import_json_1():
   result = js.create_node_from_json("Neo4j/json_files/9991001100015-TO001.json", "tomato")
   assert isinstance(result,list) and len(result) >=1

def test_import_json_2():
   result = js.create_node_from_json("Neo4j/json_files/9991000100016-CT001.json", "cut_tomato")
   assert isinstance(result,list) and len(result) >=1
