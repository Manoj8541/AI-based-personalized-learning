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


def create_roadmap(topic, time, knowledge_level):
    """
    time example: "6 Weeks"
    """

    # ============================
    # EXTRACT & CAP WEEKS (MAX 12)
    # ============================
    try:
        weeks = int(re.search(r"\d+", time).group())
    except:
        weeks = 4

    weeks = min(max(weeks, 1), 12)  # enforce 1–12 weeks

    # ============================
    # SYSTEM INSTRUCTION
    # ============================
    system_instruction = f'''
You are an AI agent who provides detailed personalized learning roadmaps.

Rules you MUST follow:
1. Generate EXACTLY {weeks} weeks (week 1 to week {weeks})
2. Each week must have:
   - topic
   - subtopics (array)
3. Each subtopic must have:
   - subtopic
   - time
   - description
4. Give more time to complex subtopics
5. Keep ALL keys lowercase
6. Output ONLY valid JSON
7. Do NOT add markdown, comments, or explanations

Example format:
{{
  "week 1": {{
    "topic": "introduction",
    "subtopics": [
      {{
        "subtopic": "basics",
        "time": "1 hour",
        "description": "learn fundamentals"
      }}
    ]
  }}
}}
'''

    # ============================
    # USER MESSAGE
    # ============================
    user_message = (
        f"Create a {weeks}-week learning roadmap for {topic}. "
        f"My knowledge level is {knowledge_level}. "
        f"I can study 16 hours per week. "
        f"Distribute topics progressively across all {weeks} weeks."
    )

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_message},
            ],
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=8192,
            top_p=0.95,
            response_format={"type": "json_object"},
        )

        response_text = chat_completion.choices[0].message.content
        print(response_text)

        roadmap = json.loads(response_text)

        # ============================
        # ✅ SAFETY POST-PROCESSING (ADDED)
        # ============================
        final_roadmap = {}
        for i in range(1, weeks + 1):
            key = f"week {i}"
            if key in roadmap:
                final_roadmap[key] = roadmap[key]

        return final_roadmap

    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Raw response: {response_text}")

        json_match = re.search(r"\{[\s\S]*\}", response_text)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass

        return {"error": "failed to parse roadmap response"}

    except Exception as e:
        print(f"Error generating roadmap: {e}")
        return {"error": str(e)}
