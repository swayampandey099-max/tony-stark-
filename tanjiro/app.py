from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

user_memories = {}

# Dictionary to map specific sentences to audio file URLs or paths
# Change the keys (sentences) and values (audio file locations) as needed
AUDIO_RESPONSES = {
    "who are you": "/tanjiro/audio/imironman.mp3",
    "send the second audio": "/static/audio/recording2.mp3",
}

SYSTEM_PROMPT = """
You are Tony Stark from Avengers.
Speak in Hinglish.
Keep replies short.
Never say you are an AI.
... (rest of your system prompt) ...
"""

def chat(user_id, message):
    # 1. Clean up user message to check for an audio trigger (case-insensitive and stripped of extra spaces)
    clean_message = message.strip().lower()
    
    for trigger_sentence, audio_path in AUDIO_RESPONSES.items():
        if clean_message == trigger_sentence.lower():
            # Return the audio file path and a boolean flag indicating it's an audio response
            return audio_path, True

    # 2. If it's not an audio trigger, proceed with the normal LLM chat logic
    if user_id not in user_memories:
        user_memories[user_id] = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

    messages = user_memories[user_id]

    messages.append({
        "role": "user",
        "content": message
    })

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    reply = response.choices[0].message.content

    messages.append({
        "role": "assistant",
        "content": reply
    })

    # Return the text reply and False (since it is not an audio file)
    return reply, False


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chatbot():
    data = request.get_json()
    message = data["message"]

    # The chat function now returns two values: the content and the type flag
    response_content, is_audio = chat("user", message)

    # Send the response along with the flag so your HTML/JS knows whether to play an audio element or display text
    return jsonify({
        "reply": response_content,
        "is_audio": is_audio
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)