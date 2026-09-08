import os
from google import genai
from google.genai import types


def generate_debate(topic):
    topic = topic.strip()

    if not topic:
        raise Exception("Please enter a debate topic.")

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise Exception("GEMINI_API_KEY is missing on the server.")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are DebateMate AI, an expert college debate coach.

EXACT DEBATE TOPIC:
{topic}

Create a complete debate preparation sheet specifically for this exact topic.

IMPORTANT:
Every section must be directly related to the exact topic.

FOR ARGUMENTS:
Give exactly 5 different arguments supporting the topic.
Each argument must focus on a different relevant aspect.

AGAINST ARGUMENTS:
Give exactly 5 different arguments opposing the topic.
Each argument must focus on a different relevant concern.

COUNTERARGUMENTS:
Give exactly 5 different counterarguments.
Each counterargument must directly challenge one of the strongest FOR arguments.
Do not simply repeat the AGAINST arguments.

REBUTTALS:
Give exactly 5 different rebuttals.
Each rebuttal must directly answer a counterargument.
Do not repeat the FOR arguments.

KEY POINTS:
Give exactly 5 short and memorable points specifically about this topic.

OPENING STATEMENT:
Write a strong 3-4 sentence opening statement specifically about this topic.

CLOSING STATEMENT:
Write a strong 3-4 sentence closing statement specifically about this topic.

STRICT RULES:
- Do not use generic or pre-written content.
- Do not repeat ideas.
- Do not repeat the same statement with different wording.
- Do not invent statistics, studies, quotations, or sources.
- Keep the language simple and suitable for college students.
- Make the content useful for an actual debate.

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

    try:
        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=1400
            )
        )

        if not response.text:
            raise Exception("Gemini returned an empty response.")

        return response.text.strip()

    except Exception as error:
        print("Gemini generation error:", repr(error))
        raise Exception(
            "Gemini generation failed. Check the Render logs for the exact API error."
        )

