from flask import Flask, jsonify, request
from flask_mongoengine import MongoEngine

from dotenv import load_dotenv
import os, sys

load_dotenv()
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

db = MongoEngine()