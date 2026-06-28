"""
Install the Groq Python SDK

$ pip install groq python-dotenv

Groq API Documentation:
https://console.groq.com/docs/quickstart
"""

import os
import re
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def generate_resources(course, knowledge_level, description, time):
    """
    Generates learning resources safely for long courses (up to 12 weeks)
    """

    # ============================
    # 🔒 SAFETY: LIMIT DESCRIPTION
    # ============================
    MAX_DESC_CHARS = 700
    safe_description = description[:MAX_DESC_CHARS]

    # ============================
    # SYSTEM PROMPT
    # ============================
    system_instruction = """
You are an expert AI tutor.

Rules you MUST follow:
1. Explain concepts clearly and step-by-step
2. Keep language calm, professional, and learner-friendly
3. Structure the content using:
   - short paragraphs
   - bullet points where useful
4. Focus ONLY on the given subtopic
5. Do NOT mention weeks, roadmap, or meta information
6. Do NOT add markdown symbols like ``` or ###
7. Output ONLY plain text
"""

    # ============================
    # USER PROMPT (TRIMMED)
    # ============================
    user_message = (
        f"Course: {course}\n"
        f"Knowledge level: {knowledge_level}\n"
        f"Time available: {time}\n\n"
        f"What the learner wants to study:\n"
        f"{safe_description}\n\n"
        f"Teach this clearly."
    )

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_message},
            ],
            model="llama-3.1-8b-instant",
            temperature=0.7,        # 🔽 more stable
            max_tokens=2048,        # 🔽 prevents overflow
            top_p=0.9,
        )

        response_text = chat_completion.choices[0].message.content
        print(response_text)

        return {
            "content": response_text
        }

    except Exception as e:
        print(f"Error generating resources: {e}")
        return {
            "content": "Unable to generate learning resources at the moment. Please try again later."
        }
