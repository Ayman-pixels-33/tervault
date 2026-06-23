import os
from google import genai
from google.genai import types
from config import get_api_key
from prompts import SEARCH_COMMAND_PROMPT as MainPrompt

def search_command(query, available_commands):
    """ابحث عن أمر"""

    api_key = get_api_key()
    if not api_key:
        print("Error: API key not set")
        return None

    client = genai.Client(api_key=api_key)
    commands_text = "\n".join([f"- {cmd[1]}: {cmd[2]}" for cmd in available_commands])

    prompt = MainPrompt.format(query=query, commands_text=commands_text)

    try:
       response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=prompt)],
                ),
            ],
        )
       return response.text
    except Exception as e:
        print(f"Error contacting Gemini API: {e}")
        return None
    

    return response.text

#if __name__ == "__main__":
#        (1, "ls -la", "List all files"),
#        (2, "pwd", "Show current directory"),
#    ]
#
 #   result = search_command("امر يقوم بتحميل البرامج الخاص بارش لينكس", test_commands)
  #  print(result)
