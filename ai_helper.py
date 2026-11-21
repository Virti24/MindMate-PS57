
from dotenv import load_dotenv
load_dotenv()

import os
from groq import Groq

SYSTEM_GUIDANCE = """You are MindMate, a warm, calm, non-judgmental
journaling companion for students.

Respond in simple, natural language. Acknowledge feelings without judging.
Do not diagnose mental health conditions or prescribe treatment.
Offer one or two gentle reflection questions or coping ideas.
Keep responses concise (100-150 words).

If the entry suggests self-harm, suicide, abuse, or immediate danger,
respond with empathy and encourage contacting a trusted person and
qualified support immediately.

In India, Tele-MANAS is available at 14416 / 1-800-891-4416.
Emergency services: 112.
Never provide methods or instructions for self-harm.
"""


def generate_supportive_reply(entry: str, mood: str, distress: bool):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return _fallback(mood, distress), True

    try:
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
           model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": SYSTEM_GUIDANCE},
                {
                    "role": "user",
                    "content": f"Mood: {mood}\nDistress: {distress}\nJournal: {entry}"
                }
            ],
            temperature=0.7,
            max_tokens=250
        )

        reply = response.choices[0].message.content

        if reply:
            return reply.strip(), False

        return _fallback(mood, distress), True

    except Exception as e:
        print("GROQ ERROR:", repr(e))
        return _fallback(mood, distress), True


def _fallback(mood: str, distress: bool) -> str:
    if distress:
        return (
            "Thank you for sharing your feelings. You deserve care and support. "
            "Please contact someone you trust. In India, Tele-MANAS is available "
            "at 14416 and emergency services at 112."
        )

    return (
        f"Thank you for checking in. You may be feeling {mood.lower()}. "
        "Give yourself time to acknowledge your feelings. "
        "What is one small thing that might make today easier?"
    )
