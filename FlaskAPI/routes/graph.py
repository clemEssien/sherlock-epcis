from flask import Flask, jsonify, request
import uuid
from flask_classful import FlaskView, route
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from neo4j import tree_algorithms as ta

class Tree(FlaskView):
    route_base = "/api/tree"

    @route("/simplepath")
    def simple_path(self):
        """
        Allows a new user to sign up and creates id info

        Request Body:
            {
                password: str,
                confirmPassword: str,
                email: str,
            }
        """
        # ta.simple_paths()

        return {"success": True}

   
