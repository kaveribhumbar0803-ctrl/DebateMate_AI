import os
import time

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

Create a complete debate preparation kit specifically for this topic.

FOR ARGUMENTS:
Give exactly 5 different arguments supporting the topic.

AGAINST ARGUMENTS:
Give exactly 5 different arguments opposing the topic.

COUNTERARGUMENTS:
Give exactly 5 counterarguments that directly challenge the strongest FOR arguments.
Do not simply repeat the AGAINST arguments.

REBUTTALS:
Give exactly 5 rebuttals that directly answer the counterarguments.
Do not repeat the FOR arguments.

KEY POINTS:
Give exactly 5 short and memorable points about this topic.

OPENING STATEMENT:
Write a strong 3-4 sentence opening statement specifically about this topic.

CLOSING STATEMENT:
Write a strong 3-4 sentence closing statement specifically about this topic.

RULES:
- Every section must be specific to the exact topic.
- Do not repeat ideas.
- Do not use generic pre-written content.
- Do not invent statistics, studies, quotations, or sources.
- Keep language simple and suitable for college students.
- Make the arguments balanced and useful for an actual debate.

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

    # Try reliable Flash models.
    models = [
        "gemini-3.6-flash",
        "gemini-3.5-flash"
    ]

    last_error = None

    for model in models:
        for attempt in range(3):
            try:
                print(
                    f"Gemini request: model={model}, attempt={attempt + 1}"
                )

                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        max_output_tokens=1400
                    )
                )

                if response and response.text:
                    print(f"Gemini success: model={model}")
                    return response.text.strip()

                raise Exception("Gemini returned an empty response.")

            except Exception as error:
                last_error = error

                print(
                    f"Gemini error: model={model}, "
                    f"attempt={attempt + 1}, error={repr(error)}"
                )

                # Wait longer after each temporary failure.
                if attempt < 2:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)

    raise Exception(
        "Gemini is temporarily unavailable. "
        "Please try Generate Debate again."
    )