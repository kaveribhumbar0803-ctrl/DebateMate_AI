import os
import json
import urllib.request
import urllib.error


def fallback_debate(topic):
    return f"""
FOR ARGUMENTS:
1. {topic} can provide several benefits when implemented properly.
2. It can improve opportunities, efficiency, and overall outcomes.
3. With responsible planning, its positive impact can be increased.

AGAINST ARGUMENTS:
1. {topic} may also create challenges or disadvantages.
2. Poor implementation can lead to unexpected problems.
3. Different people may experience different effects.

COUNTERARGUMENTS:
1. Some benefits may depend on how {topic} is implemented.
2. The disadvantages can sometimes be reduced through proper planning.
3. A balanced approach can address concerns from both sides.

REBUTTALS:
1. Even when challenges exist, they can be managed with responsible implementation.
2. The important point is to consider both benefits and risks.
3. Decisions should be based on evidence and practical outcomes.

KEY POINTS:
- Consider both advantages and disadvantages.
- Focus on evidence and logical reasoning.
- Use real examples when available.
- Present a balanced viewpoint.

OPENING STATEMENT:
Today I would like to discuss {topic} by looking at both its advantages and disadvantages.

CLOSING STATEMENT:
In conclusion, {topic} has both opportunities and challenges. A balanced and responsible approach is the best way to evaluate it.
"""


def generate_debate(topic):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return fallback_debate(topic)

    prompt = f"""
You are DebateMate AI, an expert debate coach.

Debate topic:
{topic}

Create a concise debate preparation kit.

Return exactly these sections:

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

Keep every point short, clear, student-friendly and balanced.
Do not invent statistics or sources.
"""

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.7-flash:generateContent"

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 700,
            "candidateCount": 1
        }
    }

    try:
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": api_key
            },
            method="POST"
        )

        with urllib.request.urlopen(request, timeout=45) as response:
            data = json.loads(response.read().decode("utf-8"))

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        print("Gemini API error:", e)
        return fallback_debate(topic)
