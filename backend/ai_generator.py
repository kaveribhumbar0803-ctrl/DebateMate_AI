Iimport os
import json
import urllib.request
import urllib.error


def generate_debate(topic):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise Exception("GEMINI_API_KEY is not configured on the server.")

    prompt = f"""
You are DebateMate AI, an expert debate coach.

The user entered this debate topic:

"{topic}"

Generate a complete, topic-specific debate preparation kit.

IMPORTANT RULES:
- Analyze the exact topic before generating the answer.
- Do NOT use generic or pre-written arguments.
- Every point must directly relate to the given topic.
- Give EXACTLY 5 different FOR arguments.
- Give EXACTLY 5 different AGAINST arguments.
- Give EXACTLY 5 different COUNTERARGUMENTS.
- Give EXACTLY 5 different REBUTTALS.
- Give EXACTLY 5 important KEY POINTS.
- Do not repeat ideas.
- Keep each point concise and student-friendly.
- Make the arguments logical and useful for an actual debate.
- Do not invent statistics, research papers, quotations, or sources.
- If a fact is uncertain, do not present it as a fact.

Return ONLY this format:

FOR ARGUMENTS:
1. ...
2. ...
3. ...
4. ...
5. ...

AGAINST ARGUMENTS:
1. ...
2. ...
3. ...
4. ...
5. ...

COUNTERARGUMENTS:
1. ...
2. ...
3. ...
4. ...
5. ...

REBUTTALS:
1. ...
2. ...
3. ...
4. ...
5. ...

KEY POINTS:
- ...
- ...
- ...
- ...
- ...

OPENING STATEMENT:
...

CLOSING STATEMENT:
...
"""

    url = (
        "https://generativelanguage.googleapis.com/"
        "v1beta/models/gemini-3.7-flash:generateContent"
    )

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
            "maxOutputTokens": 1200,
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

        if "candidates" not in data:
            raise Exception(
                "Gemini did not return a valid response."
            )

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="ignore")
        print("Gemini HTTP Error:", error_body)
        raise Exception(
            f"Gemini API error ({e.code}). Please try again."
        )

    except Exception as e:
        print("Gemini API Error:", e)
        raise Exception(
            "Unable to generate the debate kit. Please try again."
        )
