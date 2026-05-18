from .tools import tools
from .tools.discovery_tools import describe_scene
from dotenv import load_dotenv
from google.genai import Client
from dataclasses import dataclass
from .system_prompt import system_prompt
from .context import set_scene_id, set_db_session
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from google.genai.types import GenerateContentConfig

load_dotenv()

@dataclass
class ToolCallData:
    id: str
    name: str
    args: Dict[str, Any]
    response: Optional[Dict[str, Any]] = None

@dataclass
class AgentResponseData:
    text: str
    tool_calls: List[ToolCallData]
    thoughts: str

def extract_response_data(parts, afc_history=None) -> AgentResponseData:
    text_segments = []
    tool_calls: List[ToolCallData] = []
    thoughts = []

    # 1. Process final response parts
    for part in parts:
        if part.text:
            text_segments.append(part.text)
        
        # If AFC is disabled, tool calls might be here
        if part.function_call:
            args = part.function_call.args
            if hasattr(args, "items"):
                args = {k: v for k, v in args.items()}
            tool_calls.append(ToolCallData(
                id=part.function_call.id if hasattr(part.function_call, "id") else "",
                name=part.function_call.name,
                args=args
            ))
            
        if part.thought:
            thoughts.append(str(part.thought) + "\n")
        elif hasattr(part, "thought_signature") and part.thought_signature:
            thoughts.append(str(part.thought_signature) + "\n")

    # 2. Process Automatic Function Calling history (if it exists)
    if afc_history:
        for history_content in afc_history:
            for part in history_content.parts:
                
                # A. The Model decides to call a tool
                if history_content.role == "model":
                    if part.function_call:
                        args = part.function_call.args
                        if hasattr(args, "items"):
                            args = {k: v for k, v in args.items()}
                        tool_calls.append(ToolCallData(
                            id=part.function_call.id if hasattr(part.function_call, "id") else "",
                            name=part.function_call.name,
                            args=args
                        ))
                    
                    if part.thought:
                        thoughts.append(str(part.thought) + "\n")
                    elif hasattr(part, "thought_signature") and part.thought_signature:
                        thoughts.append(str(part.thought_signature) + "\n")
                        
                # B. The SDK (User) returns the tool response
                elif history_content.role == "user":
                    if part.function_response:
                        # Find the last tool call with matching name that lacks a response
                        for tc in reversed(tool_calls):
                            if tc.name == part.function_response.name and tc.response is None:
                                tc.response = part.function_response.response
                                break

    return AgentResponseData(
        text="".join(text_segments),
        tool_calls=tool_calls,
        thoughts="".join(thoughts)
    )

async def gemini_agent(
    messages: List[dict],
    client: Client,
    db: AsyncSession,
    scene_id: str,
) -> AgentResponseData:
    # Inject context so tool functions can access db and scene_id
    set_db_session(db)
    set_scene_id(scene_id)

    scene_desc = await describe_scene()
    instruction = system_prompt(scene_desc)

    try:
        response = await client.aio.models.generate_content(
            contents=messages,
            model="gemini-3.1-flash-lite",
            config=GenerateContentConfig(
                system_instruction=instruction,
                tools=tools,
            )
        )

        usage = response.usage_metadata
        if usage:
            print(f"\n📊 Tokens: {usage.total_token_count} (Input: {usage.prompt_token_count} | Output: {usage.candidates_token_count})")

        parts = response.candidates[0].content.parts
        afc_history = getattr(response, "automatic_function_calling_history", None)
        extracted_data = extract_response_data(parts, afc_history)

        if extracted_data.text:
            print(f"\n🤖 Assistant: {extracted_data.text}\n")

        # Crucial: Append the original parts to maintain tool call context
        messages.append({"role": "model", "parts": parts})
        
        return extracted_data

    except Exception as e:
        print(f"\n[Error querying Gemini]: {e}")
        return AgentResponseData(text="", tool_calls=[], thoughts="")