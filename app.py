from flask import Flask, render_template_string, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=API_KEY) if API_KEY else None

SYSTEM_PROMPT = """You are the official AI assistant of La Ola Rooftop in Casablanca.

La Ola: "Ocean in sight. Music on all night. A rooftop for music lovers, free spirits & good appetites."

KEY INFO:
- Address: 12 Bd de l'Ocean Atlantique, Ain Diab, Casablanca
- Phone: 05 22 79 78 85
- Hours: Every day 09:30 to 01:00
- Instagram: @laolarooftop
- Links: linktr.ee/laolarooftop
- Community: LA OLA FAMILY 656 members

MENU highlights:
- Aperol Spritz 90 DH
- Seafood Pizza 100 DH
- Gambas 90 DH
- Full menu: story highlight FOOD AND DRINKS on @laolarooftop

EVENTS:
- Wunderbar Music - Thursday
- La Brava Party - Wednesday
- Ola's Voice karaoke - Tuesday at 21:00
- Sunday Jam - Every Sunday
- Lila Gnawia - Coming soon

RESERVATIONS:
- 1-3 people: no reservation needed, first come first served
- 4+ people: reservation recommended via DM or call 05 22 79 78 85

RULES:
- Be warm, chill, like real La Ola staff
- Use Mrehba occasionally
- Reply in same language as user (French or English)
- Max 3-4 lines per reply
- Never say I don't know
- Always make La Ola sound like THE place to be
- If lonely or alone: be extra warm and welcoming
- Events start at 21:00 by default
"""

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>La Ola Assistant</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;1,300&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
font-family: 'DM Sans', sans-serif;
background: #0d2535;
min-height: 100vh;
display: flex;
align-items: center;
justify-content: center;
overflow: hidden;
position: relative;
}
body::before {
content: '';
position: fixed;
inset: 0;
background: radial-gradient(ellipse at 20% 80%, rgba(45,106,122,0.45) 0%, transparent 55%),
radial-gradient(ellipse at 80% 20%, rgba(201,169,110,0.1) 0%, transparent 50%),
linear-gradient(160deg, #091c29 0%, #0d2535 45%, #122e3e 100%);
z-index: 0;
}
.container {
position: relative;
z-index: 1;
width: 100%;
max-width: 440px;
height: 100vh;
display: flex;
flex-direction: column;
}
.header {
padding: 22px 20px 16px;
text-align: center;
background: rgba(9,28,41,0.8);
backdrop-filter: blur(20px);
border-bottom: 1px solid rgba(201,169,110,0.15);
flex-shrink: 0;
}
.logo-row { display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 2px; }
.brand { font-family: 'Cormorant Garamond', serif; font-size: 28px; font-weight: 300; letter-spacing: 0.2em; color: #e8dcc8; }
.brand em { color: #c9a96e; font-style: italic; }
.status { display: inline-flex; align-items: center; gap: 6px; font-size: 11px; color: rgba(232,220,200,0.5); }
.dot { width: 6px; height: 6px; border-radius: 50%; background: #4ade80; }
.messages { flex: 1; overflow-y: auto; padding: 16px 14px; display: flex; flex-direction: column; gap: 12px; scrollbar-width: none; }
.msg { max-width: 85%; }
.msg.bot { align-self: flex-start; }
.msg.user { align-self: flex-end; }
.msg-label { font-size: 9.5px; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 5px; color: rgba(201,169,110,0.5); }
.bubble { padding: 12px 16px; border-radius: 18px; font-size: 13.5px; line-height: 1.65; }
.msg.bot .bubble { background: rgba(255,255,255,0.055); border: 1px solid rgba(201,169,110,0.16); color: #e8dcc8; border-radius: 4px 18px 18px 18px; }
.msg.user .bubble { background: linear-gradient(135deg, #c9a96e, #b8924a); color: #111; border-radius: 18px 18px 4px 18px; }
.quick-wrap { padding: 6px 14px 10px; display: flex; flex-wrap: wrap; gap: 7px; }
.q-btn { padding: 7px 14px; border-radius: 22px; border: 1px solid rgba(201,169,110,0.28); background: rgba(201,169,110,0.06); color: #c9a96e; font-size: 12px; cursor: pointer; }
.input-area { padding: 10px 14px 20px; background: rgba(9,28,41,0.85); border-top: 1px solid rgba(201,169,110,0.1); }
.input-row { display: flex; align-items: center; gap: 8px; background: rgba(232,220,200,0.05); border: 1px solid rgba(201,169,110,0.2); border-radius: 28px; padding: 5px 5px 5px 16px; }
input { flex: 1; background: none; border: none; outline: none; color: #e8dcc8; font-size: 14px; }
.send-btn { width: 38px; height: 38px; border-radius: 50%; border: none; background: linear-gradient(135deg, #c9a96e, #b8924a); color: #0d2535; cursor: pointer; font-weight: 700; }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div class="logo-row">
      <div class="brand">La <em>Ola</em></div>
    </div>
    <div class="status"><span class="dot"></span> Disponible 24h/24</div>
  </div>
  <div class="messages" id="chat">
    <div class="msg bot">
      <div class="msg-label">La Ola</div>
      <div class="bubble">Mrehba! 🌊<br>Bienvenue à La Ola Rooftop. How can I help you?</div>
    </div>
  </div>
  <div class="quick-wrap" id="quickWrap">
    <button class="q-btn" onclick="qs('menu')">Menu</button>
    <button class="q-btn" onclick="qs('reservation')">Réservation</button>
    <button class="q-btn" onclick="qs('location')">Adresse</button>
  </div>
  <div class="input-area">
    <div class="input-row">
      <input id="inp" placeholder="Ask anything..." onkeypress="if(event.key==='Enter')send()">
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
  d.innerHTML = '<div class="msg-label">' + (who === "bot" ? "La Ola" : "Vous") + '</div><div class="bubble">' + text + '</div>';
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
    addMsg("Mrehba 😅<br><br>Petit bug technique. Appelez-nous directement : 05 22 79 78 85", "bot");
  }
}
function qs(text) { document.getElementById("inp").value = text; send(); }
</script>
</body>
</html>"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    msg = data.get("message", "").strip()
    hist = data.get("history", [])
    m = msg.lower()

    PHONE = "05 22 79 78 85"
    LINK = "<a href='https://linktr.ee/laolarooftop' target='_blank' style='color:#c9a96e'>linktr.ee/laolarooftop</a>"
    INSTA = "<strong>@laolarooftop</strong>"

    # --- UPDATED RESPONSES (VERSION UPGRADE) ---

    if any(x in m for x in ["menu", "food", "eat", "manger", "plat", "dish", "drink", "boire", "carte", "prix", "price"]):
        return jsonify({"reply": "🔥 Our favourites:<br><br>🍤 Gambas - 90 DH<br>🍕 Seafood Pizza - 100 DH<br>🍹 Aperol Spritz - 90 DH<br><br>Full menu on " + INSTA + " (Highlights: FOOD AND DRINKS)"})

    if any(x in m for x in ["location", "where", "adresse", "address", "corniche", "ain diab"]):
        return jsonify({"reply": "📍 12 Bd de l'Ocean Atlantique, Ain Diab, Casablanca.<br><br>Right on the corniche, ocean in sight! 🌊"})

    if any(x in m for x in ["reserv", "book", "table", "place", "resa"]):
        return jsonify({"reply": "Nice choice 👀<br><br>1-3 people: First come, first served.<br>4+ people: Call us at " + PHONE + " or DM " + INSTA})

    if any(x in m for x in ["event", "soiree", "tonight", "programme", "dj", "music", "karaoke", "jam", "gnawia", "brava", "wunderbar"]):
        return jsonify({"reply": "🎶 DJ sets & live vibes daily!<br><br>Tue: Karaoke 🎤<br>Wed: La Brava 💃<br>Sun: Jam Session 🎸<br><br>Check " + LINK + " for details."})

    if any(x in m for x in ["horaire", "heure", "open", "close", "ouvert", "ferme", "hours", "when", "quand", "time", "reopen"]):
        return jsonify({"reply": "🕙 Open every day from 09:30 to 01:00.<br><br>From morning coffee to late night drinks 🌊"})

    # --- AI FALLBACK ---
    if client:
        try:
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            messages += hist[-6:] if hist else [{"role": "user", "content": msg}]
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                max_tokens=150,
                temperature=0.75
            )
            return jsonify({"reply": response.choices[0].message.content})
        except Exception:
            pass
    
    return jsonify({"reply": "Mrehba 😊<br><br>Pour toute question ou réservation, contactez-nous : " + PHONE + " ou DM " + INSTA})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
