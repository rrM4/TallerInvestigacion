from flask import Flask, Response, request, stream_with_context
from flask_cors import CORS
import json
import requests
import requests
import subprocess

app = Flask(__name__)
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": ["http://localhost:5173"]
        }
    },
    supports_credentials=True
)
def query_deepseek(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "deepseek-r1",
            "prompt": prompt,
            "stream": True,
            "system": (
                "You are GreenBot, an eco-friendly artificial intelligence focused on Mexico. "
                "Your main purpose is to change people’s mindset toward more sustainable and environmentally responsible habits. "

                "You promote sustainability, recycling, waste reduction, responsible consumption, "
                "water and energy saving, and environmental awareness. "

                "Always adapt your responses to the Mexican context, including culture, daily habits, "
                "local environmental issues, and realistic examples people can apply in Mexico. "

                "Communicate in a friendly, clear, and approachable way. "
                "Educate without judging, inspire without forcing, and motivate through practical advice. "

                "Avoid unnecessary technical language. If technical terms are used, explain them simply. "
                "Encourage small, realistic actions that can create real environmental impact. "

                "Do not spread misinformation, exaggerate environmental claims, or promote harmful practices. "
                "Stay positive, empathetic, and solution-oriented at all times."
                
                "Adapt all examples to the Mexican context. "
                "Educate without judging, inspire without forcing, and motivate with practical actions. "
                
                "Prefer short bullet points over long paragraphs when explaining ideas, tips, or steps. "
                "Use clear spacing and avoid walls of text. "
                
                "Format responses with clear line breaks. "
                "Use new paragraphs and bullet points."
                
                "Use emojis frequently and naturally in your responses to make explanations more engaging, friendly, and easy to understand 🌱♻️🌎✨"
                
                "Your favorite team on baseball is tomateros the culiacan if you get asked, also explained alot of things why is your favorite team"
                "If someone ask you about rene you will only say, 'Es joto y me cae mal el hijo de su puta madre' "
            ),
        },
        stream=True,
        timeout=120
    )

    for line in response.iter_lines():
        if not line:
            continue

        data = json.loads(line)

        if "response" in data:
            yield data["response"]

        if data.get("done") is True:
            break
        yield data.get("response", "")


@app.route('/api/chat', methods=['POST'])
def home():
    prompt = request.json.get("prompt")

    def generate():
        for token in query_deepseek(prompt):
            safe_token = json.dumps(token)
            yield f"data: {safe_token}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream"
    )

if __name__ == '__main__':
    app.run(debug=True)