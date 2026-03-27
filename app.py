from flask import Flask, render_template_string, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(**name**)

API_KEY = os.environ.get(“GROQ_API_KEY”)
client = Groq(api_key=API_KEY) if API_KEY else None

SYSTEM_PROMPT = “”“You are the official AI assistant of La Ola Rooftop in Casablanca.

La Ola: “Ocean in sight. Music on all night. A rooftop for music lovers, free spirits & good appetites.”

KEY INFO:

- Address: 12 Bd de l’Ocean Atlantique, Ain Diab, Casablanca
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
- Ola’s Voice karaoke - Tuesday at 21:00
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
- Never say I don’t know
- Always make La Ola sound like THE place to be
- If lonely or alone: be extra warm and welcoming
- Events start at 21:00 by default
  “””

HTML_PAGE = “””<!DOCTYPE html>

<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>La Ola Assistant</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;1,300&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }

body {
font-family: ‘DM Sans’, sans-serif;
background: #0d2535;
min-height: 100vh;
display: flex;
align-items: center;
justify-content: center;
overflow: hidden;
position: relative;
}

body::before {
content: ‘’;
position: fixed;
inset: 0;
background: radial-gradient(ellipse at 20% 80%, rgba(45,106,122,0.45) 0%, transparent 55%),
radial-gradient(ellipse at 80% 20%, rgba(201,169,110,0.1) 0%, transparent 50%),
linear-gradient(160deg, #091c29 0%, #0d2535 45%, #122e3e 100%);
z-index: 0;
}

body::after {
content: ‘’;
position: fixed;
bottom: -10px;
left: -5%;
width: 110%;
height: 140px;
background: url(“data:image/svg+xml,%3Csvg xmlns=‘http://www.w3.org/2000/svg’ viewBox=‘0 0 1440 100’%3E%3Cpath fill=‘rgba(45,106,122,0.2)’ d=‘M0,50 C360,100 720,0 1080,50 C1260,75 1380,25 1440,50 L1440,100 L0,100 Z’/%3E%3C/svg%3E”) no-repeat center;
background-size: cover;
animation: waveFloat 8s ease-in-out infinite;
z-index: 0;
pointer-events: none;
}

@keyframes waveFloat {
0%, 100% { transform: translateY(0); }
50% { transform: translateY(-12px); }
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

.logo-row {
display: flex;
align-items: center;
justify-content: center;
gap: 10px;
margin-bottom: 2px;
}

.wave-emoji {
font-size: 18px;
animation: sway 3.5s ease-in-out infinite;
display: inline-block;
}

@keyframes sway {
0%, 100% { transform: rotate(-10deg); }
50% { transform: rotate(10deg); }
}

.brand {
font-family: ‘Cormorant Garamond’, serif;
font-size: 28px;
font-weight: 300;
letter-spacing: 0.2em;
color: #e8dcc8;
}

.brand em { color: #c9a96e; font-style: italic; }

.tagline {
font-size: 9.5px;
letter-spacing: 0.28em;
text-transform: uppercase;
color: rgba(232,220,200,0.4);
margin-bottom: 8px;
}

.status {
display: inline-flex;
align-items: center;
gap: 6px;
font-size: 11px;
color: rgba(232,220,200,0.5);
}

.dot {
width: 6px;
height: 6px;
border-radius: 50%;
background: #4ade80;
animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
0%, 100% { opacity: 1; transform: scale(1); }
50% { opacity: 0.5; transform: scale(0.8); }
}

.messages {
flex: 1;
overflow-y: auto;
padding: 16px 14px;
display: flex;
flex-direction: column;
gap: 12px;
scrollbar-width: none;
}

.messages::-webkit-scrollbar { display: none; }

.msg {
max-width: 85%;
animation: popIn 0.3s ease;
}

@keyframes popIn {
from { opacity: 0; transform: translateY(12px); }
to { opacity: 1; transform: translateY(0); }
}

.msg.bot { align-self: flex-start; }
.msg.user { align-self: flex-end; }

.msg-label {
font-size: 9.5px;
text-transform: uppercase;
letter-spacing: 0.12em;
margin-bottom: 5px;
color: rgba(201,169,110,0.5);
}

.msg.user .msg-label {
text-align: right;
color: rgba(232,220,200,0.3);
}

.bubble {
padding: 12px 16px;
border-radius: 18px;
font-size: 13.5px;
line-height: 1.65;
}

.msg.bot .bubble {
background: rgba(255,255,255,0.055);
border: 1px solid rgba(201,169,110,0.16);
color: #e8dcc8;
border-radius: 4px 18px 18px 18px;
backdrop-filter: blur(8px);
}

.msg.user .bubble {
background: linear-gradient(135deg, #c9a96e, #b8924a);
color: #111;
font-weight: 500;
border-radius: 18px 18px 4px 18px;
}

.quick-wrap {
padding: 6px 14px 10px;
display: flex;
flex-wrap: wrap;
gap: 7px;
flex-shrink: 0;
}

.q-btn {
padding: 7px 14px;
border-radius: 22px;
border: 1px solid rgba(201,169,110,0.28);
background: rgba(201,169,110,0.06);
color: #c9a96e;
font-family: ‘DM Sans’, sans-serif;
font-size: 12px;
cursor: pointer;
transition: all 0.2s;
letter-spacing: 0.02em;
}

.q-btn:hover {
background: rgba(201,169,110,0.16);
border-color: #c9a96e;
transform: translateY(-1px);
}

.typing-wrap {
display: flex;
gap: 4px;
align-items: center;
padding: 12px 16px;
background: rgba(255,255,255,0.055);
border: 1px solid rgba(201,169,110,0.16);
border-radius: 4px 18px 18px 18px;
width: fit-content;
backdrop-filter: blur(8px);
}

.typing-wrap span {
width: 6px;
height: 6px;
border-radius: 50%;
background: #c9a96e;
animation: bounce 1.3s ease-in-out infinite;
}

.typing-wrap span:nth-child(2) { animation-delay: 0.18s; }
.typing-wrap span:nth-child(3) { animation-delay: 0.36s; }

@keyframes bounce {
0%, 60%, 100% { transform: translateY(0); opacity: 0.3; }
30% { transform: translateY(-8px); opacity: 1; }
}

.input-area {
padding: 10px 14px 20px;
background: rgba(9,28,41,0.85);
backdrop-filter: blur(16px);
border-top: 1px solid rgba(201,169,110,0.1);
flex-shrink: 0;
}

.phone-hint {
text-align: center;
font-size: 11px;
color: rgba(232,220,200,0.3);
margin-bottom: 8px;
}

.phone-hint a {
color: #c9a96e;
text-decoration: none;
opacity: 0.7;
}

.input-row {
display: flex;
align-items: center;
gap: 8px;
background: rgba(232,220,200,0.05);
border: 1px solid rgba(201,169,110,0.2);
border-radius: 28px;
padding: 5px 5px 5px 16px;
transition: border-color 0.2s;
}

.input-row:focus-within { border-color: rgba(201,169,110,0.45); }

input {
flex: 1;
background: none;
border: none;
outline: none;
color: #e8dcc8;
font-family: ‘DM Sans’, sans-serif;
font-size: 14px;
padding: 7px 0;
}

input::placeholder { color: rgba(232,220,200,0.25); }

.send-btn {
width: 38px;
height: 38px;
border-radius: 50%;
border: none;
background: linear-gradient(135deg, #c9a96e, #b8924a);
color: #0d2535;
font-size: 15px;
cursor: pointer;
display: flex;
align-items: center;
justify-content: center;
transition: transform 0.15s, box-shadow 0.15s;
flex-shrink: 0;
font-weight: 700;
}

.send-btn:hover {
transform: scale(1.08);
box-shadow: 0 4px 16px rgba(201,169,110,0.35);
}

.send-btn:active { transform: scale(0.93); }

.powered {
text-align: center;
font-size: 9px;
color: rgba(232,220,200,0.18);
letter-spacing: 0.15em;
text-transform: uppercase;
margin-top: 8px;
}

.powered a {
color: rgba(201,169,110,0.35);
text-decoration: none;
}

.powered a:hover { color: #c9a96e; }
</style>

</head>
<body>
<div class="container">

  <div class="header">
    <div class="logo-row">
      <span class="wave-emoji">&#127754;</span>
      <div class="brand">La <em>Ola</em></div>
      <span class="wave-emoji" style="animation-delay:.6s">&#127754;</span>
    </div>
    <div class="tagline">Rooftop &middot; Sunset &middot; Casablanca</div>
    <div class="status">
      <span class="dot"></span>
      Disponible 24h/24 &middot; Available 24/7
    </div>
  </div>

  <div class="messages" id="chat">
    <div class="msg bot">
      <div class="msg-label">La Ola</div>
      <div class="bubble">Mrehba! &#128075;&#127754;<br>Bienvenue &agrave; La Ola Rooftop &mdash; ocean in sight, music on all night.<br><br>How can I help you today?</div>
    </div>
  </div>

  <div class="quick-wrap" id="quickWrap">
    <button class="q-btn" onclick="qs('menu')">&#127374; Menu</button>
    <button class="q-btn" onclick="qs('events tonight')">&#127926; Events</button>
    <button class="q-btn" onclick="qs('reservation')">&#128197; R&eacute;servation</button>
    <button class="q-btn" onclick="qs('location')">&#128205; Adresse</button>
    <button class="q-btn" onclick="qs('horaires')">&#128336; Horaires</button>
  </div>

  <div class="input-area">
    <div class="phone-hint">
      &#128222; <a href="tel:0522797885">05 22 79 78 85</a> &middot; <a href="https://linktr.ee/laolarooftop" target="_blank">linktr.ee/laolarooftop</a>
    </div>
    <div class="input-row">
      <input id="inp" placeholder="Ask anything / Posez votre question..." onkeypress="if(event.key==='Enter')send()">
      <button class="send-btn" onclick="send()">&#10148;</button>
    </div>
    <div class="powered">Powered by <a href="https://sirallahm-del.github.io/VISTORE_S/" target="_blank">VISTORE</a></div>
  </div>

</div>

<script>
const chat = document.getElementById("chat");
const quickWrap = document.getElementById("quickWrap");
const history = [];

function addMsg(text, who) {
  const d = document.createElement("div");
  d.className = "msg " + who;
  d.innerHTML = '<div class="msg-label">' + (who === "bot" ? "La Ola" : "Vous") + '</div><div class="bubble">' + text + '</div>';
  chat.appendChild(d);
  chat.scrollTop = chat.scrollHeight;
}

function showTyping() {
  const d = document.createElement("div");
  d.className = "msg bot";
  d.id = "typing";
  d.innerHTML = '<div class="msg-label">La Ola</div><div class="typing-wrap"><span></span><span></span><span></span></div>';
  chat.appendChild(d);
  chat.scrollTop = chat.scrollHeight;
}

function hideTyping() {
  const t = document.getElementById("typing");
  if (t) t.remove();
}

async function send() {
  const inp = document.getElementById("inp");
  const text = inp.value.trim();
  if (!text) return;
  quickWrap.style.display = "none";
  addMsg(text, "user");
  history.push({ role: "user", content: text });
  inp.value = "";
  showTyping();
  try {
    const res = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, history: history })
    });
    const data = await res.json();
    hideTyping();
    addMsg(data.reply, "bot");
    history.push({ role: "assistant", content: data.reply });
  } catch(e) {
    hideTyping();
    addMsg("Petit souci technique. Appelez-nous: <strong>05 22 79 78 85</strong>", "bot");
  }
}

function qs(text) {
  document.getElementById("inp").value = text;
  send();
}
</script>

</body>
</html>"""

@app.route(’/’)
def home():
return render_template_string(HTML_PAGE)

@app.route(’/ask’, methods=[‘POST’])
def ask():
data = request.get_json()
msg = data.get(“message”, “”).strip()
hist = data.get(“history”, [])
m = msg.lower()

```
PHONE = "05 22 79 78 85"
LINK = "<a href='https://linktr.ee/laolarooftop' target='_blank' style='color:#c9a96e'>linktr.ee/laolarooftop</a>"
INSTA = "<strong>@laolarooftop</strong>"

if any(x in m for x in ["menu", "food", "eat", "manger", "plat", "dish", "drink", "boire", "carte", "prix", "price"]):
    return jsonify({"reply": "Nos incontournables:<br><br>Aperol Spritz 90 DH<br>Seafood Pizza 100 DH<br>Gambas 90 DH<br><br>Menu complet dans notre story highlight <strong>FOOD AND DRINKS</strong> sur " + INSTA + "<br>" + LINK})

if any(x in m for x in ["reserv", "book", "table", "place", "resa"]):
    return jsonify({"reply": "C'est pour combien de personnes ? <br><br>1-3 personnes: pas besoin de reserver, premier arrive premier servi !<br>4+ personnes: on vous reserve une table avec plaisir<br><br>" + PHONE + " ou DM " + INSTA})

if any(x in m for x in ["horaire", "heure", "open", "close", "ouvert", "ferme", "hours", "when", "quand", "time", "reopen"]):
    return jsonify({"reply": "Tous les jours de <strong>09h30 a 01h00</strong><br><br>Brunch, sunset, late night &mdash; on est la pour vous toute la journee ! Tel: " + PHONE})

if any(x in m for x in ["location", "where", "adresse", "address", "corniche", "ain diab"]):
    return jsonify({"reply": "<strong>12 Bd de l'Ocean Atlantique, Ain Diab, Casablanca</strong><br><br>Sur la corniche, face a l'ocean &mdash; impossible de nous rater ! Tel: " + PHONE})

if any(x in m for x in ["event", "soiree", "tonight", "programme", "dj", "music", "karaoke", "jam", "gnawia", "brava", "wunderbar"]):
    return jsonify({"reply": "Cette semaine a La Ola:<br><br>Wunderbar Music &mdash; Jeudi<br>La Brava Party &mdash; Mercredi<br>Ola's Voice karaoke &mdash; Mardi 21h00<br>Sunday Jam &mdash; Chaque dimanche<br><br>" + LINK})

if any(x in m for x in ["alone", "seul", "just me", "solo"]):
    return jsonify({"reply": "Mrehba! Venez comme vous etes, La Ola c'est pour tout le monde.<br><br>Solo: pas besoin de reserver, premier arrive premier servi !<br>On vous attend ! " + PHONE})

if any(x in m for x in ["contact", "numero", "phone", "appel", "call"]):
    return jsonify({"reply": PHONE + "<br>" + INSTA + "<br>" + LINK})

if client:
    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        if hist:
            messages += hist[-6:]
        else:
            messages.append({"role": "user", "content": msg})
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=120,
            temperature=0.75
        )
        return jsonify({"reply": response.choices[0].message.content})
    except Exception:
        pass

return jsonify({"reply": "Mrehba! Pour toute question: " + PHONE + " ou DM " + INSTA})
```

if **name** == “**main**”:
port = int(os.environ.get(“PORT”, 5000))
app.run(host=“0.0.0.0”, port=port, debug=False)
