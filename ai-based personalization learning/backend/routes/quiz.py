from flask import Blueprint, jsonify, request
from ..quiz import get_quiz

quiz_bp = Blueprint("quiz", __name__)


@quiz_bp.route("/generate", methods=["POST"])
def generate_quiz():
    req = request.get_json()
    
    course = req.get("course")
    topic = req.get("topic")
    subtopic = req.get("subtopic")
    description = req.get("description")
    
    if not req:
        return jsonify({"error": "Invalid JSON body"}), 400

    if not (course and topic and subtopic and description):
        return jsonify({"error": "Required fields not provided"}), 400
    
    quiz_data = get_quiz(course, topic, subtopic, description)
    return jsonify(quiz_data)