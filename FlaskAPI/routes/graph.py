import json
from flask import Flask, jsonify, request
import uuid
import os
import sys
from flask_classful import FlaskView, route

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
upperlevel = os.path.dirname(parentdir)
sys.path.append(upperlevel)

from Neo4j import tree_algorithms as ta 


class Tree(FlaskView):
    route_base = "/api/tree"

    @route("/simplepath", methods=["GET"])
    def simple_path(self):
        """
        Returns the all simple paths between two events

        Request Body:
            {
                source_event_id: str,
                source_event_label: str,
                destination_event_id: str,
                destination_event_label: str,
                relationship: str
            }
        """
        response = ta.simple_paths('de61ba3f-5d59-4902-82f4-44e200e7b676','TransformationEvent',
        'a2624953-f2e6-4369-8e71-9ee1a19d81d5','AggregationEvent','NEXT')
        
        if isinstance(response, list):
            return {"success": True}, 200
        else:
            return {"error": "No path returned"}, 400 

    @route("/shortestpath", methods=["GET"])
    def shortest_path(self):
        """
        Returns the all simple paths between two events
        
        Request Body:
            {
                source_event_id: str,
                source_event_label: str,
                destination_event_id: str,
                destination_event_label: str,
                relationship: str
            }
        """

        response = ta.shortest_path('de61ba3f-5d59-4902-82f4-44e200e7b676','TransformationEvent',
        'a2624953-f2e6-4369-8e71-9ee1a19d81d5','AggregationEvent','NEXT')
       
        if isinstance(response, list):
            return {"success": True}, 200
        else:
            return {"error": "No path returned"}, 400 
   
    @route("/forward_trace", methods=["GET"])
    def forward_trace(self):
        """
        Returns the path for forward trace from a source event
        
        Request Body:
            {
                source_event_id: str,
                source_event_label: str,
                relationship: str
            }
        """

        response = ta.forward_trace('de61ba3f-5d59-4902-82f4-44e200e7b676','TransformationEvent','NEXT')
        print(response)
        if isinstance(response, list):
            return {"success": True}, 200
        else:
            return {"error": "No path returned"}, 400 

    @route("/backward_trace", methods=["GET"])
    def backward_trace(self):
        """
        Returns the path for backward trace from a source event
        
        Request Body:
            {
                source_event_id: str,
                source_event_label: str,
                relationship: str
            }
        """

        response = ta.backward_trace('de61ba3f-5d59-4902-82f4-44e200e7b676','TransformationEvent','NEXT')
        print(response)
        if isinstance(response, list):
            return {"success": True}, 200
        else:
            return {"error": "No path returned"}, 400 