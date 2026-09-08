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
You are DebateMate AI, a college debate coach.

TOPIC:
{topic}

Create a debate preparation kit specifically for this topic.

Give EXACTLY:

FOR ARGUMENTS:
5 different supporting arguments.

AGAINST ARGUMENTS:
5 different opposing arguments.

COUNTERARGUMENTS:
5 responses challenging the strongest FOR arguments.
Do not copy the AGAINST arguments.

REBUTTALS:
5 responses to the counterarguments.
Do not copy the FOR arguments.

KEY POINTS:
5 short important points.

OPENING STATEMENT:
3 sentences.

CLOSING STATEMENT:
3 sentences.

RULES:
- Everything must be specifically related to the topic.
- Keep language simple for college students.
- Do not repeat ideas.
- Do not invent statistics or sources.
- Be balanced.
- Return ONLY the requested sections.

FORMAT:

FOR ARGUMENTS:
1.
2.
3.
4.
5.

AGAINST ARGUMENTS:
1.
2.
3.
4.
5.

COUNTERARGUMENTS:
1.
2.
3.
4.
5.

REBUTTALS:
1.
2.
3.
4.
5.

KEY POINTS:
- 
- 
- 
- 
- 

OPENING STATEMENT:
...

CLOSING STATEMENT:
...
"""

    # Current stable models.
    models = [
        "gemini-3.8-flash",
        "gemini-3.5-flash-lite",
        "gemini-2.5-flash-lite"
    ]

    last_error = None

    for model in models:
        for attempt in range(2):
            try:
                print(
                    f"Trying Gemini model: {model}, "
                    f"attempt: {attempt + 1}"
                )

                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.7,
                        max_output_tokens=1200
                    )
                )

                if response is not None and response.text:
                    print(f"Gemini success: {model}")
                    return response.text.strip()

                raise Exception("Gemini returned an empty response.")

            except Exception as error:
                last_error = error

                print(
                    f"Gemini failed: {model}, "
                    f"attempt: {attempt + 1}, "
                    f"error: {repr(error)}"
                )

                if attempt == 0:
                    time.sleep(3)

    print("All Gemini models failed.")
    print("Last Gemini error:", repr(last_error))

    raise Exception(
        "Gemini is temporarily unavailable. "
        "Please try again in a few seconds."
    )