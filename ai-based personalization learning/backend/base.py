from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS

from database.db import get_db, init_db
from database.auth import auth

import roadmap
import quiz
import generativeResources
import translate

api = Flask(__name__)
CORS(api)
init_db()    
api.register_blueprint(auth)

@api.route("/api/roadmap", methods=["POST"])
def get_roadmap():
    req = request.get_json()
    if not req:
        return jsonify({"error": "Invalid JSON body"}), 400

    response_body = roadmap.create_roadmap(
        topic=req.get("topic", "Machine Learning"),
        time=req.get("time", "4 weeks"),
        knowledge_level=req.get("knowledge_level", "Absolute Beginner"),
    )

    return jsonify(response_body)


@api.route("/api/quiz", methods=["POST"])
def get_quiz():
    req = request.get_json()
    if not req:
        return jsonify({"error": "Invalid JSON body"}), 400

    course = req.get("course")
    topic = req.get("topic")
    subtopic = req.get("subtopic")
    description = req.get("description")

    if not (course and topic and subtopic and description):
        return jsonify({"error": "Required fields not provided"}), 400

    print("getting quiz...")
    response_body = quiz.get_quiz(course, topic, subtopic, description)
    return jsonify(response_body)


@api.route("/api/translate", methods=["POST"])
def get_translations():
    req = request.get_json()
    if not req:
        return jsonify({"error": "Invalid JSON body"}), 400

    text = req.get("textArr")
    to_lang = req.get("toLang")

    if not (text and to_lang):
        return jsonify({"error": "Required fields not provided"}), 400

    print(f"Translating to {to_lang}: {text}")
    translated_text = translate.translate_text_arr(
        text_arr=text,
        target=to_lang
    )

    return jsonify(translated_text)


@api.route("/api/generate-resource", methods=["POST"])
def generative_resource():
    req = request.get_json()
    if not req:
        return jsonify({"error": "Invalid JSON body"}), 400

    required_fields = ["course", "knowledge_level", "description", "time"]
    for field in required_fields:
        if not req.get(field):
            return jsonify({"error": "Required fields not provided"}), 400

    print(f"generative resources for {req['course']}")

    resources = generativeResources.generate_resources(
        course=req["course"],
        knowledge_level=req["knowledge_level"],
        description=req["description"],
        time=req["time"],
    )

    return jsonify(resources)


if __name__ == "__main__":
    api.run(debug=True)