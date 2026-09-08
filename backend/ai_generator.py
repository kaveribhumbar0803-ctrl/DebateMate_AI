import os
import json
import time
import urllib.request
import urllib.error


MODEL = "gemini-3.7-flash"
API_URL = (
    f"https://generativelanguage.googleapis.com/"
    f"v1beta/models/{MODEL}:generateContent"
)


def generate_debate(topic):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise Exception("GEMINI_API_KEY is not configured on the server.")

    topic = topic.strip()

    if not topic:
        raise Exception("Debate topic cannot be empty.")

    prompt = f"""
You are DebateMate AI, a professional debate coach.

DEBATE TOPIC:
"{topic}"

Create a complete and highly specific debate preparation sheet for THIS EXACT TOPIC.

IMPORTANT:
Every section must be based specifically on the topic above.
Do not use generic arguments.
Do not repeat the same idea in different wording.

Generate:

FOR ARGUMENTS:
Exactly 5 different arguments supporting the topic.
Each argument must focus on a different aspect such as benefits, practicality,
society, education, economy, technology, ethics, safety, or future impact,
whichever are actually relevant to the topic.

AGAINST ARGUMENTS:
Exactly 5 different arguments opposing the topic.
Each must focus on a different relevant concern or disadvantage.

COUNTERARGUMENTS:
Exactly 5 responses to the strongest FOR arguments.
Each counterargument must directly challenge a specific FOR argument.
Do not simply repeat the AGAINST section.

REBUTTALS:
Exactly 5 responses defending the FOR side against the counterarguments.
Each rebuttal must answer a different counterargument.
Make them logical and convincing.

KEY POINTS:
Exactly 5 short, memorable points that summarize the most important ideas
of THIS topic for a student preparing for a debate.

OPENING STATEMENT:
Write a strong 3-4 sentence opening statement specifically about this topic.
It should introduce the issue and clearly establish the debate position.

CLOSING STATEMENT:
Write a strong 3-4 sentence closing statement specifically about this topic.
It should summarize the main reasoning and end with a convincing conclusion.

STRICT RULES:
- Never use generic filler.
- Never repeat the same argument.
- Counterarguments must directly answer FOR arguments.
- Rebuttals must directly answer counterarguments.
- Opening and closing statements must mention the actual topic.
- Do not invent statistics, studies, quotations, or sources.
- Keep the language student-friendly.
- Make the content useful for an actual college debate.

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
                "role": "user",
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.8,
            "maxOutputTokens": 1400,
            "candidateCount": 1
        }
    }

    request_data = json.dumps(payload).encode("utf-8")

    last_error = None

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

            with urllib.request.urlopen(request, timeout=60) as response:
                raw_response = response.read().decode("utf-8")

            data = json.loads(raw_response)

            if "error" in data:
                error_message = data["error"].get(
                    "message",
                    "Unknown Gemini API error."
                )
                print("Gemini API Error:", error_message)
                raise Exception(error_message)

            candidates = data.get("candidates")

            if not candidates:
                raise Exception("Gemini returned no candidates.")

            content = candidates[0].get("content", {})
            parts = content.get("parts", [])

            if not parts:
                raise Exception("Gemini returned no text.")

            text = parts[0].get("text", "").strip()

            if not text:
                raise Exception("Gemini returned an empty response.")

            return text

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="ignore")
            print("Gemini HTTP Error:", e.code)
            print("Gemini Response:", error_body)

            last_error = f"Gemini API HTTP {e.code}"

            # Retry temporary server/rate-limit errors.
            if e.code in (429, 500, 502, 503, 504) and attempt == 0:
                time.sleep(2)
                continue

            raise Exception(
                f"Gemini API error ({e.code}). Please try again."
            )

        except urllib.error.URLError as e:
            print("Gemini Connection Error:", e)

            last_error = "Unable to connect to Gemini API."

            if attempt == 0:
                time.sleep(2)
                continue

            raise Exception(last_error)

        except Exception as e:
            print("Gemini Error:", e)
            last_error = str(e)

            if attempt == 0:
                time.sleep(2)
                continue

            raise Exception(last_error)

    raise Exception(last_error or "Unable to generate the debate kit.")

Why this should stop the problem

Your previous code was asking Gemini for a very large response containing 30+ separate pieces of content. Now the request is more controlled, and temporary "429/500/502/503/504" failures are retried once.

Also, your API authentication method is correct according to Google's current documentation.

Important: Don't change "app.py", "evaluator.py", frontend files, Render settings, or your API key for this fix.

Just replace "backend/ai_generator.py" with the code above. Then save it.

Stop there. Tell me Done, and I'll give you only the next step.