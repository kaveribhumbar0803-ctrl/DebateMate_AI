import os
import json
import urllib.request
import urllib.error


def generate_debate(topic):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise Exception("GEMINI_API_KEY is not configured on the server.")

    prompt = f"""
You are DebateMate AI, an expert debate coach.

DEBATE TOPIC:
"{topic}"

Your task is to deeply analyze this EXACT topic and create a high-quality,
topic-specific debate preparation kit.

IMPORTANT:
Every argument MUST be specifically about the given topic.
Do not use generic statements that could apply to any debate topic.

DIVERSITY RULE:
Each point must introduce a DIFFERENT IDEA or DIMENSION.
Do NOT rewrite the same argument using different words.

For example, if one point discusses cost, another point must NOT simply
say that the topic is economically beneficial in different words.
Use different aspects such as education, society, ethics, technology,
employment, privacy, safety, accessibility, human impact, implementation,
long-term effects, etc., ONLY when relevant to the actual topic.

REQUIREMENTS:

1. FOR ARGUMENTS
Give EXACTLY 5 strong arguments supporting the topic.
Each must use a different relevant aspect of the topic.

2. AGAINST ARGUMENTS
Give EXACTLY 5 strong arguments opposing the topic.
Each must use a different relevant aspect of the topic.

3. COUNTERARGUMENTS
Give EXACTLY 5 responses that directly challenge the strongest AGAINST
arguments.
Each counterargument must address a different concern.

4. REBUTTALS
Give EXACTLY 5 responses defending the AGAINST side against the FOR side.
Each rebuttal must address a different argument.

5. KEY POINTS
Give EXACTLY 5 memorable debate points.
Each must highlight a different important aspect of the topic.

QUALITY RULES:
- Analyze the exact wording and meaning of the topic first.
- Do not use generic or pre-written arguments.
- Do not repeat ideas.
- Do not make one sentence appear in multiple sections.
- Do not invent statistics, studies, quotations, or sources.
- If a specific fact is uncertain, avoid presenting it as fact.
- Keep arguments concise but meaningful.
- Make the content useful for an actual student debate.
- Use clear, student-friendly language.
- Do not mention that you are an AI.
- Do not add explanations outside the requested structure.

Return ONLY this structure:

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
            "temperature": 0.8,
            "maxOutputTokens": 1600,
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
            raise Exception("Gemini did not return a valid response.")

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