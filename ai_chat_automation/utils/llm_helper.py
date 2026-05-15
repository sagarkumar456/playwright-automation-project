from openai import OpenAI

# YOUR ACTUAL API KEY HERE
API_KEY = "api key"


client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def get_ai_reply(bot_message, test_case_scenario):
    prompt = f"""You are roleplaying as a real customer talking to a support chatbot.

Here is your Test Case/Persona details:
{test_case_scenario}

The Chatbot just asked you: "{bot_message}"

Based ONLY on your Test Case details, provide the most natural and brief reply to the chatbot. 

Rules:
1. Provide ONLY the answer text. No extra words, no quotes, no explanations.
2. Keep it short. If the bot asks for a name, just give the name. If it asks for a number, just give the number.
3. If the bot simply says "Hi" or "Hello" without a question, reply with "Hi".
4. If the bot asks "How can I help you?", state your main issue.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    return response.choices[0].message.content.strip()