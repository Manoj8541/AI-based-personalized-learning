"""
Install the Groq Python SDK

$ pip install groq python-dotenv

Groq API Documentation:
https://console.groq.com/docs/quickstart
"""

import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def get_quiz(course, topic, subtopic, description):
    """
    Generates MCQ quiz safely even for long courses (>4 weeks)
    """

    # ============================
    # 🔒 SAFETY: LIMIT DESCRIPTION
    # ============================
    MAX_DESC_CHARS = 600
    safe_description = description[:MAX_DESC_CHARS]

    # ============================
    # SYSTEM PROMPT
    # ============================
    system_instruction = """
You are an expert AI quiz generator.

Rules you MUST follow:
1. Generate 5–8 multiple choice questions
2. Questions must test understanding, not memory
3. Each question MUST include:
   - question
   - options (array)
   - answerIndex (number)
   - reason (short explanation)
4. Keep all keys lowercase
5. Output ONLY valid JSON
6. No markdown, no commentary, no explanations outside JSON

Format:
{
  "questions": [
    {
      "question": "...",
      "options": ["a", "b", "c", "d"],
      "answerIndex": 1,
      "reason": "..."
    }
  ]
}
"""

    # ============================
    # USER PROMPT (TRIMMED)
    # ============================
    user_message = (
        f"Course: {course}\n"
        f"Topic: {topic}\n"
        f"Subtopic: {subtopic}\n"
        f"What the learner studied:\n{safe_description}\n"
        f"Create a quiz based ONLY on this."
    )

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_message},
            ],
            model="llama-3.1-8b-instant",
            temperature=0.6,          # 🔽 more stable
            max_tokens=2048,          # 🔽 prevent overflow
            top_p=0.9,
            response_format={"type": "json_object"},
        )

        response_text = chat_completion.choices[0].message.content
        print(response_text)

        return json.loads(response_text)

    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Raw response: {response_text}")

        json_match = re.search(r"\{[\s\S]*\}", response_text)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass

        return {"questions": [], "error": "failed to parse quiz response"}

    except Exception as e:
        print(f"Error generating quiz: {e}")
        return {"questions": [], "error": str(e)}
