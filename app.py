from flask import Flask, render_template_string, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=API_KEY) if API_KEY else None

SYSTEM_PROMPT = """You are the official AI assistant of La Ola Rooftop in Casablanca.
Style: Warm, chill, professional but friendly. Use "Mrehba" occasionally.
Location: 12 Bd de l'Ocean Atlantique, Ain Diab.
Phone: 05 22 79 78 85.
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
      <div class="bubble">Mrehba! 🌊<br>Bienvenue à La Ola Rooftop. How can I help you today?</div>
    </div>
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
  d.innerHTML = '<div class="bubble">' + text + '</div>';
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
    addMsg("Mrehba 😅 Bug technique. Appelle-nous : 05 22 79 78 85", "bot");
  }
}
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
    INSTA = "@laolarooftop"

    # --- 1. EXISTING QUICK CONDITIONS ---
    if any(x in m for x in ["menu", "food", "eat", "manger"]):
        return jsonify({"reply": "🔥 Our favourites:<br><br>🍤 Gambas — 90 DH<br>🍕 Seafood Pizza — 100 DH<br>🍹 Aperol Spritz — 90 DH<br><br>Perfect for sharing with drinks 😉<br><br>You coming for food or drinks?"})

    if any(x in m for x in ["drink", "cocktail", "boire", "spritz"]):
        return jsonify({"reply": "🍸 For drinks, it’s perfect around sunset.<br><br>Aperol Spritz, cocktails & ocean view — best combo.<br><br>You coming with friends or just chilling?"})

    if any(x in m for x in ["location", "where", "adresse", "address"]):
        return jsonify({"reply": "📍 We're right on the corniche — 12 Bd de l'Ocean Atlantique.<br><br>Super easy to find, ocean front 😊<br><br>You coming tonight?"})

    # --- 2. NEW SALES UPGRADES (Time, View, Busy, Group) ---

    # TIME / WHEN TO COME
    if any(x in m for x in ["time", "when", "quand", "heure"]):
        return jsonify({"reply": "⏰ Best time really depends on the vibe.<br><br>Around sunset (7-8pm) is perfect for drinks.<br>After 9pm it gets more lively with music 🎶<br><br>You looking for chill or more party?"})

    # VIEW / TERRACE
    if any(x in m for x in ["view", "terrace", "vue", "outside", "ocean"]):
        return jsonify({"reply": "Yesss 🌊 the rooftop view is unmatched.<br><br>Ocean view, sunset, music... perfect vibe honestly.<br><br>You planning for drinks or dinner?"})

    # IS IT BUSY / CROWD
    if any(x in m for x in ["busy", "crowd", "monde", "rempli"]):
        return jsonify({"reply": "Yeah it gets quite busy at night 🔥<br><br>But that's when the vibe is best 😉<br>If you want a good spot, I'd recommend booking.<br><br>You coming tonight?"})

    # GROUP / 4+ PEOPLE
    if any(x in m for x in ["4", "four", "quatre", "group", "plusieurs", "amis", "friends"]):
        return jsonify({"reply": "Nice 👀 for 4+ people I'd recommend booking.<br><br>It gets pretty busy, especially at night 🔥<br>You can DM or call — they'll sort you out.<br><br>What time are you thinking?"})

    # --- 3. AI PART (MUST BE LAST) ---
    if client:
        try:
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            messages += hist[-6:] if hist else [{"role": "user", "content": msg}]
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                max_tokens=150
            )
            return jsonify({"reply": response.choices[0].message.content})
        except Exception:
            pass
    
    return jsonify({"reply": "Mrehba! Pour toute info : " + PHONE + " ou DM sur Insta " + INSTA})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
