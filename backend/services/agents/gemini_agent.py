from typing import List
from .tools import tools
from dotenv import load_dotenv
from google.genai import Client
from .system_prompt import system_prompt
from google.genai.types import GenerateContentConfig

load_dotenv()

instruction = system_prompt()

async def gemini_agent(messages: List[dict], client: Client):
    try:
        response = await client.aio.models.generate_content(
            contents=messages,
            model="gemini-3.1-flash-lite-preview",
                config=GenerateContentConfig(
                system_instruction=instruction,
                tools=tools,
            )
        )

        usage = response.usage_metadata
        print(f"\nðŸ“Š Tokens: {usage.total_token_count} (Input: {usage.prompt_token_count} | Output: {usage.candidates_token_count})")

        if response.text:
            print(f"\nðŸ¤– Assistant: {response.text}\n")

        messages.append({"role": "model", "parts": response.candidates[0].content.parts})

    except Exception as e:
        print(f"\n[Error querying Gemini]: {e}")