from flask import Blueprint, jsonify, request
from .model import GlobalModel

api = Blueprint('api', __name__)
global_model = GlobalModel()

@api.route('/model', methods=['GET'])
def get_global_model():
    try:
        return global_model.send_model()
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Server error"}), 500

@api.route('/update', methods=['POST'])
def update_global_model():
    try:
        client_data = request.data
        global_model.receive_update(client_data)
        return jsonify({"status": "Update received"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
