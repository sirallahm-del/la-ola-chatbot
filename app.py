from flask import Flask, render_template_string, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=API_KEY) if API_KEY else None

SYSTEM_PROMPT = """You are a real human assistant for La Ola rooftop.

Talk like a real person texting.
Keep it VERY short (1-2 sentences max).

No marketing talk.
No long explanations.

Be chill, natural, friendly.

Always ask a small question at the end.
"""

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>La Ola 🌊</title>

<style>
body {
font-family: Arial;
background: linear-gradient(180deg, #091c29, #0d2535);
color: white;
margin: 0;
}

.chat {
max-width: 500px;
margin: auto;
height: 100vh;
display: flex;
flex-direction: column;
}

.messages {
flex: 1;
overflow-y: auto;
padding: 20px;
}

.msg {
padding: 12px;
border-radius: 12px;
margin: 8px 0;
max-width: 80%;
}

.bot { background: #1e293b; }
.user { background: #c9a96e; color: black; margin-left: auto; }

.quick {
display: flex;
gap: 10px;
flex-wrap: wrap;
padding: 10px;
}

.quick button {
background: #c9a96e;
border: none;
padding: 8px 12px;
border-radius: 8px;
cursor: pointer;
}

.input {
display: flex;
padding: 10px;
}

input {
flex: 1;
padding: 10px;
}

button.send {
padding: 10px;
background: #c9a96e;
border: none;
}
</style>
</head>

<body>
<div class="chat">

<div class="messages" id="chat">
<div class="msg bot">
Hey 👋 welcome to La Ola 🌊<br><br>
What can I help you with?
</div>
</div>

<div class="quick">
<button onclick="quickMsg('menu')">Menu 🍽️</button>
<button onclick="quickMsg('book')">Book 📅</button>
<button onclick="quickMsg('location')">Location 📍</button>
<button onclick="quickMsg('events')">Events 🎶</button>
</div>

<div class="input">
<input id="input" placeholder="Ask anything..." onkeypress="if(event.key==='Enter')send()">
<button class="send" onclick="send()">→</button>
</div>

</div>

<script>
async function send(){
const input = document.getElementById("input");
const chat = document.getElementById("chat");

const text = input.value;
if(!text) return;

chat.innerHTML += `<div class="msg user">${text}</div>`;
input.value = "";

const res = await fetch("/ask", {
method:"POST",
headers: {"Content-Type":"application/json"},
body: JSON.stringify({message:text})
});

const data = await res.json();

chat.innerHTML += `<div class="msg bot">${data.reply}</div>`;
chat.scrollTop = chat.scrollHeight;
}

function quickMsg(text){
document.getElementById("input").value = text;
send();
}
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/ask', methods=['POST'])
def ask():
    msg = request.json.get("message", "").lower()

    # ===== SMART FIX PROBLEM =====
    if any(x in msg for x in ["problem", "issue", "complaint", "bug"]):
        return jsonify({
            "reply": "Ah sorry about that 🙏 what happened?"
        })

    # ===== RÉPONSES RAPIDES =====

    if "menu" in msg:
        return jsonify({
            "reply": """🔥 Popular:<br>
🍹 Aperol Spritz — 90 DH<br>
🍕 Seafood Pizza — 100 DH<br>
🍤 Gambas — 90 DH<br><br>
You more drinks or food? 😄"""
        })

    if any(x in msg for x in ["location", "where", "adresse"]):
        return jsonify({
            "reply": """📍 12 Bd de l’Océan Atlantique, Ain Diab 🌊<br><br>
Right on the corniche 😉<br><br>
You coming tonight?"""
        })

    if "book" in msg:
        return jsonify({
            "reply": """Nice 👀<br><br>
DM @laolarooftop 📩<br><br>
How many people?"""
        })

    if "event" in msg:
        return jsonify({
            "reply": """DJ sets every night 🎶🔥<br><br>
Best after 8pm 👀<br><br>
You more chill or party?"""
        })

    if any(x in msg for x in ["hour", "open", "close", "time"]):
        return jsonify({
            "reply": """We’re open every day 09:30 → 01:00 🕒<br><br>
You thinking brunch or night vibe?"""
        })

    # ===== IA =====

    if client:
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": msg}
                ],
                max_tokens=80,
                temperature=0.8
            )

            reply = response.choices[0].message.content
            return jsonify({"reply": reply})

        except:
            pass

    return jsonify({
        "reply": "Hey 👋 you looking for menu, booking, location or events?"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)