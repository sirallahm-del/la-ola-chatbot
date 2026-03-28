# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=API_KEY) if API_KEY else None

# --- SYSTEM PROMPT ULTIME ---
SYSTEM_PROMPT = """You are the top guest relations manager at La Ola Rooftop Casablanca.
Your goal is to guide users to confirm their reservation via phone or WhatsApp.
Rules:
- Never pretend a booking is confirmed.
- Always guide toward calling (05 22 79 78 85) or WhatsApp (+212 767-393109).
- For the full menu, tell them to check our Instagram Highlights (@laolarooftop).
- Keep replies short, natural, premium.
- Always end with a question or action.
Style: Chill luxury vibe. Use "Mrehba" naturally. Use emojis subtly (🔥 👌 🌊).
"""

HTML_PAGE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>La Ola Assistant</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;1,300&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'DM Sans', sans-serif; background: #0d2535; min-height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden; position: relative; }
body::before { content: ''; position: fixed; inset: 0; background: radial-gradient(ellipse at 20% 80%, rgba(45,106,122,0.45) 0%, transparent 55%), radial-gradient(ellipse at 80% 20%, rgba(201,169,110,0.1) 0%, transparent 50%), linear-gradient(160deg, #091c29 0%, #0d2535 45%, #122e3e 100%); z-index: 0; }
.container { position: relative; z-index: 1; width: 100%; max-width: 440px; height: 100vh; display: flex; flex-direction: column; }
.header { padding: 22px 20px 16px; text-align: center; background: rgba(9,28,41,0.8); backdrop-filter: blur(20px); border-bottom: 1px solid rgba(201,169,110,0.15); flex-shrink: 0; }
.brand { font-family: 'Cormorant Garamond', serif; font-size: 28px; font-weight: 300; letter-spacing: 0.2em; color: #e8dcc8; }
.brand em { color: #c9a96e; font-style: italic; }
.messages { flex: 1; overflow-y: auto; padding: 16px 14px; display: flex; flex-direction: column; gap: 12px; scrollbar-width: none; }
.msg { max-width: 85%; }
.msg.bot { align-self: flex-start; }
.msg.user { align-self: flex-end; }
.bubble { padding: 12px 16px; border-radius: 18px; font-size: 13.5px; line-height: 1.65; }
.msg.bot .bubble { background: rgba(255,255,255,0.055); border: 1px solid rgba(201,169,110,0.16); color: #e8dcc8; border-radius: 4px 18px 18px 18px; }
.msg.user .bubble { background: linear-gradient(135deg, #c9a96e, #b8924a); color: #111; border-radius: 18px 18px 4px 18px; }
.bubble a { color: #c9a96e; font-weight: 700; text-decoration: underline; }
.quick-wrap { padding: 10px 14px; display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; }
.q-btn { padding: 8px 16px; border-radius: 20px; border: 1px solid rgba(201,169,110,0.3); background: rgba(201,169,110,0.1); color: #c9a96e; font-size: 12px; cursor: pointer; transition: 0.3s; }
.q-btn:hover { background: rgba(201,169,110,0.2); }
.input-area { padding: 10px 14px 20px; background: rgba(9,28,41,0.85); border-top: 1px solid rgba(201,169,110,0.1); }
.input-row { display: flex; align-items: center; gap: 8px; background: rgba(232,220,200,0.05); border: 1px solid rgba(201,169,110,0.2); border-radius: 28px; padding: 5px 5px 5px 16px; }
input { flex: 1; background: none; border: none; outline: none; color: #e8dcc8; font-size: 14px; }
.send-btn { width: 38px; height: 38px; border-radius: 50%; border: none; background: linear-gradient(135deg, #c9a96e, #b8924a); color: #0d2535; cursor: pointer; font-weight: 700; }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div class="brand">La <em>Ola</em></div>
  </div>
  <div class="messages" id="chat">
    <div class="msg bot">
      <div class="bubble">Mrehba! 🌊<br>I'm here to handle your night at La Ola. What's the plan?</div>
    </div>
  </div>
  <div class="quick-wrap">
    <button class="q-btn" onclick="qs('Book a table')">📅 Book a table</button>
    <button class="q-btn" onclick="qs('Menu & Drinks')">🍹 Menu & Drinks</button>
    <button class="q-btn" onclick="qs('Location')">📍 Location</button>
  </div>
  <div class="input-area">
    <div class="input-row">
      <input id="inp" placeholder="Message La Ola..." onkeypress="if(event.key==='Enter')send()">
      <button class="send-btn" onclick="send()">➔</button>
    </div>
  </div>
</div>
<script>
const chat = document.getElementById("chat");
const history = [];
function addMsg(text, who) {
  const d = document.createElement("div");
  d.className = "msg " + who;
  // Correction du replace pour les sauts de ligne
  d.innerHTML = '<div class="bubble">' + text.replace(/\\n/g, "<br>").replace(/\\n/g, "<br>") + '</div>';
  chat.appendChild(d);
  chat.scrollTop = chat.scrollHeight;
}
async function send() {
  const inp = document.getElementById("inp");
  const text = inp.value.trim();
  if (!text) return;
  addMsg(text, "user");
  history.push({ role: "user", content: text });
  inp.value = "";
  try {
    const res = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, history: history })
    });
    const data = await res.json();
    addMsg(data.reply, "bot");
    history.push({ role: "assistant", content: data.reply });
  } catch(e) {
    addMsg("Mrehba 👌 Appelez-nous au 05 22 79 78 85 ou via <a href='https://wa.me/212767393109' target='_blank'>WhatsApp</a>.", "bot");
  }
}
function qs(val) { document.getElementById("inp").value = val; send(); }
</script>
</body>
</html>"""

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    msg = data.get("message", "").strip()
    hist = data.get("history", [])
    m = msg.lower()
    
    PHONE = "05 22 79 78 85"
    WA_LINK = "https://wa.me/212767393109"
    MAPS_LINK = "https://maps.app.goo.gl/YourActualLink" # Remplace par ton lien réel Ain Diab

    # --- RÉPONSES PRIORITAIRES ---
    if any(x in m for x in ["book", "table", "reserve", "booking"]):
        return jsonify({"reply": f"Perfect 👌<br><br><a href='{WA_LINK}' target='_blank'>👉 Book via WhatsApp</a><br><br>Or call: {PHONE}. How many people?"})

    if any(x in m for x in ["location", "where", "adresse", "trouver"]):
        return jsonify({"reply": f"Mrehba! 🌊 We are in Ain Diab.<br><br><a href='{MAPS_LINK}' target='_blank'>📍 Open in Google Maps</a><br><br>See you tonight?"})

    if any(x in m for x in ["menu", "food", "drink"]):
        return jsonify({"reply": "🔥 Favorites: Gambas (90DH), Seafood Pizza (100DH).<br><br><a href='https://www.instagram.com/laolarooftop/' target='_blank'>📸 View Full Menu on Instagram</a><br><br>Ready to book?"})

    # --- AI BACKUP ---
    if client:
        try:
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            messages += hist[-6:]
            response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=messages, max_tokens=150)
            return jsonify({"reply": response.choices[0].message.content})
        except: pass
    
    return jsonify({"reply": f"Mrehba! Call {PHONE} or <a href='{WA_LINK}' target='_blank'>WhatsApp us</a> to confirm. 🔥"})

@app.route('/')
def home(): return render_template_string(HTML_PAGE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
