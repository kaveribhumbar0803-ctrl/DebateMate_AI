import os
import json
import time
import urllib.request
import urllib.error


MODEL = "gemini-3.7-flash"

API_URL = (
    "https://generativelanguage.googleapis.com/"
    "v1beta/models/" + MODEL + ":generateContent"
)


def generate_debate(topic):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise Exception("GEMINI_API_KEY is not configured on the server.")

    topic = topic.strip()

    if not topic:
        raise Exception("Debate topic cannot be empty.")

    prompt = """
You are DebateMate AI, an expert debate coach.

The exact debate topic is:

""" + topic + """

Create a complete debate preparation kit specifically for this topic.

IMPORTANT RULES:

1. Give exactly 5 FOR arguments.
2. Give exactly 5 AGAINST arguments.
3. Give exactly 5 COUNTERARGUMENTS.
4. Give exactly 5 REBUTTALS.
5. Give exactly 5 KEY POINTS.
6. Write a topic-specific OPENING STATEMENT.
7. Write a topic-specific CLOSING STATEMENT.

Every point must be directly related to the exact topic.

Do NOT use generic arguments.
Do NOT repeat the same idea.
Do NOT repeat an argument using different words.

COUNTERARGUMENTS must respond directly to the FOR arguments.

REBUTTALS must respond directly to the COUNTERARGUMENTS.

KEY POINTS must summarize the most important ideas about this exact topic.

The OPENING STATEMENT must clearly introduce this exact topic.

The CLOSING STATEMENT must clearly conclude this exact topic.

Do not invent statistics, studies, quotations, or sources.

Use simple, clear language suitable for a college student.

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
            "temperature": 0.8,
            "maxOutputTokens": 1400
        }
    }

    request_data = json.dumps(payload).encode("utf-8")

    for attempt in range(2):
        try:
            request = urllib.request.Request(
                API_URL,
                data=request_data,
                headers={
                    "Content-Type": "application/json",
                    "x-goog-api-key": api_key
                },
                method="POST"
            )

            with urllib.request.urlopen(
                request,
                timeout=60
            ) as response:

                response_text = response.read().decode("utf-8")

            data = json.loads(response_text)

            if "error" in data:
                message = data["error"].get(
                    "message",
                    "Unknown Gemini API error."
                )

                print("Gemini API Error:", message)

                raise Exception(message)

            candidates = data.get("candidates", [])

            if not candidates:
                raise Exception(
                    "Gemini returned no candidates."
                )

            content = candidates[0].get("content", {})
            parts = content.get("parts", [])

            if not parts:
                raise Exception(
                    "Gemini returned no text."
                )

            result = parts[0].get("text", "").strip()

            if not result:
                raise Exception(
                    "Gemini returned an empty response."
                )

            return result

        except urllib.error.HTTPError as error:
            error_body = error.read().decode(
                "utf-8",
                errors="ignore"
            )

            print("Gemini HTTP Error:", error.code)
            print("Gemini Response:", error_body)

            if error.code in (429, 500, 502, 503, 504):
                if attempt == 0:
                    time.sleep(2)
                    continue

            raise Exception(
                "Gemini API error: HTTP "
                + str(error.code)
            )

        except urllib.error.URLError as error:
            print("Gemini connection error:", error)

            if attempt == 0:
                time.sleep(2)
                continue

            raise Exception(
                "Unable to connect to Gemini API."
            )

        except Exception as error:
            print("Gemini error:", error)

            if attempt == 0:
                time.sleep(2)
                continue

            raise Exception(str(error))

    raise Exception(
        "Unable to generate the debate kit."
    )

