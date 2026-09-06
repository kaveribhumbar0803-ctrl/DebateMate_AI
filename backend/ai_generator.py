from google import genai
import os

# Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_debate(topic):
    prompt = f"""
You are DebateMate AI, an expert debate coach.

Debate topic:
{topic}

Create a useful debate preparation kit.

Return the answer in exactly this structure:

FOR ARGUMENTS:
1. ...
2. ...
3. ...

AGAINST ARGUMENTS:
1. ...
2. ...
3. ...

COUNTERARGUMENTS:
1. ...
2. ...
3. ...

REBUTTALS:
1. ...
2. ...
3. ...

KEY POINTS:
- ...
- ...
- ...

OPENING STATEMENT:
...

CLOSING STATEMENT:
...

Keep the information student-friendly, clear, balanced and concise.
Do not invent statistics or sources.
"""

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=prompt
    )

    return response.text