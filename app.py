from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(**name**)

HTML_PAGE = “””

<!DOCTYPE html>

<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>La Ola — Assistant</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root { --sand: #e8dcc8; --ocean: #0d2535; --gold: #c9a96e; --gold2: #b8924a; }

body {
font-family: ‘DM Sans’, sans-serif;
background: var(–ocean);
min-height: 100vh;
display: flex;
align-items: center;
justify-content: center;
overflow: hidden;
}

body::before {
content: ‘’;
position: fixed;
inset: 0;
background:
radial-gradient(ellipse at 15% 85%, rgba(45,106,122,0.5) 0%, transparent 55%),
radial-gradient(ellipse at 85% 15%, rgba(201,169,110,0.12) 0%, transparent 50%),
linear-gradient(160deg, #091c29 0%, #0d2535 45%, #122e3e 100%);
z-index: 0;
}

body::after {
content: ‘’;
position: fixed;
bottom: -10px;
left: -5%;
width: 110%;
height: 160px;
background: url(“data:image/svg+xml,%3Csvg xmlns=‘http://www.w3.org/2000/svg’ viewBox=‘0 0 1440 100’%3E%3Cpath fill=‘rgba(45,106,122,0.25)’ d=‘M0,50 C360,100 720,0 1080,50 C1260,75 1380,25 1440,50 L1440,100 L0,100 Z’/%3E%3C/svg%3E”) no-repeat center;
background-size: cover;
animation: waveFloat 7s ease-in-out infinite;
z-index: 0;
pointer-events: none;
}

@keyframes waveFloat {
0%, 100% { transform: translateY(0); }
50% { transform: translateY(-10px); }
}

.container {
position: relative;
z-index: 1;
width: 100%;
max-width: 430px;
height: 100vh;
display: flex;
flex-direction: column;
}

.header {
padding: 24px 20px 18px;
text-align: center;
background: rgba(9,28,41,0.75);
backdrop-filter: blur(16px);
border-bottom: 1px solid rgba(201,169,110,0.18);
flex-shrink: 0;
}

.logo-row {
display: flex;
align-items: center;
justify-content: center;
gap: 10px;
margin-bottom: 3px;
}

.wave-emoji {
font-size: 20px;
animation: sway 3s ease-in-out infinite;
display: inline-block;
}

@keyframes sway {
0%, 100% { transform: rotate(-8deg); }
50% { transform: rotate(8deg); }
}

.brand-name {
font-family: ‘Cormorant Garamond’, serif;
font-size: 30px;
font-weight: 300;
letter-spacing: 0.18em;
color: var(–sand);
}

.brand-name em { color: var(–gold); font-style: italic; }

.tagline {
font-size: 10px;
letter-spacing: 0.25em;
text-transform: uppercase;
color: rgba(232,220,200,0.45);
}

.status-badge {
display: inline-flex;
align-items: center;
gap: 6px;
margin-top: 8px;
font-size: 11px;
color: rgba(232,220,200,0.55);
}

.dot {
width: 7px; height: 7px;
border-radius: 50%;
background: #4ade80;
animation: blink 2s ease-in-out infinite;
}

@keyframes blink {
0%, 100% { opacity: 1; }
50% { opacity: 0.4; }
}

.messages {
flex: 1;
overflow-y: auto;
padding: 18px 14px;
display: flex;
flex-direction: column;
gap: 10px;
scrollbar-width: none;
}
.messages::-webkit-scrollbar { display: none; }

.msg { max-width: 84%; animation: popIn 0.25s ease; }

@keyframes popIn {
from { opacity: 0; transform: translateY(10px); }
to { opacity: 1; transform: translateY(0); }
}

.msg.bot { align-self: flex-start; }
.msg.user { align-self: flex-end; }

.label {
font-size: 10px;
text-transform: uppercase;
letter-spacing: 0.1em;
margin-bottom: 4px;
color: rgba(201,169,110,0.55);
}

.msg.user .label { text-align: right; color: rgba(232,220,200,0.35); }

.bubble {
padding: 11px 15px;
border-radius: 18px;
font-size: 14px;
line-height: 1.6;
}

.msg.bot .bubble {
background: rgba(255,255,255,0.06);
border: 1px solid rgba(201,169,110,0.18);
color: var(–sand);
border-radius: 4px 18px 18px 18px;
backdrop-filter: blur(6px);
}

.msg.user .bubble {
background: linear-gradient(135deg, var(–gold), var(–gold2));
color: #111;
font-weight: 500;
border-radius: 18px 18px 4px 18px;
}

.quick-wrap {
padding: 4px 14px 10px;
display: flex;
flex-wrap: wrap;
gap: 8px;
flex-shrink: 0;
}

.q-btn {
padding: 7px 15px;
border-radius: 22px;
border: 1px solid rgba(201,169,110,0.3);
background: rgba(201,169,110,0.07);
color: var(–gold);
font-family: ‘DM Sans’, sans-serif;
font-size: 12.5px;
cursor: pointer;
transition: all 0.2s;
}

.q-btn:hover { background: rgba(201,169,110,0.18); border-color: var(–gold); }

.typing-bubble {
display: inline-flex;
gap: 5px;
align-items: center;
padding: 13px 18px;
background: rgba(255,255,255,0.06);
border: 1px solid rgba(201,169,110,0.18);
border-radius: 4px 18px 18px 18px;
}

.typing-bubble span {
width: 7px; height: 7px;
border-radius: 50%;
background: var(–gold);
animation: typingBounce 1.2s ease-in-out infinite;
}
.typing-bubble span:nth-child(2) { animation-delay: 0.15s; }
.typing-bubble span:nth-child(3) { animation-delay: 0.3s; }

@keyframes typingBounce {
0%, 60%, 100% { transform: translateY(0); opacity: 0.35; }
30% { transform: translateY(-7px); opacity: 1; }
}

.input-area {
padding: 10px 14px 22px;
background: rgba(9,28,41,0.8);
backdrop-filter: blur(14px);
border-top: 1px solid rgba(201,169,110,0.12);
flex-shrink: 0;
}

.input-row {
display: flex;
align-items: center;
gap: 8px;
background: rgba(232,220,200,0.06);
border: 1px solid rgba(201,169,110,0.22);
border-radius: 30px;
padding: 5px 5px 5px 18px;
transition: border-color 0.2s;
}

.input-row:focus-within { border-color: rgba(201,169,110,0.5); }

input {
flex: 1;
background: none;
border: none;
outline: none;
color: var(–sand);
font-family: ‘DM Sans’, sans-serif;
font-size: 14px;
padding: 7px 0;
}

input::placeholder { color: rgba(232,220,200,0.28); }

.send {
width: 40px; height: 40px;
border-radius: 50%;
border: none;
background: linear-gradient(135deg, var(–gold), var(–gold2));
color: #111;
font-size: 16px;
cursor: pointer;
display: flex;
align-items: center;
justify-content: center;
transition: transform 0.15s;
flex-shrink: 0;
}

.send:hover { transform: scale(1.08); }
.send:active { transform: scale(0.93); }
</style>

</head>
<body>
<div class="container">
  <div class="header">
    <div class="logo-row">
      <span class="wave-emoji">🌊</span>
      <div class="brand-name">La <em>Ola</em></div>
      <span class="wave-emoji" style="animation-delay:0.5s">🌊</span>
    </div>
    <div class="tagline">Rooftop · Casablanca · Ain Diab</div>
    <div class="status-badge"><span class="dot"></span>Available 24/7</div>
  </div>

  <div class="messages" id="chat">
    <div class="msg bot">
      <div class="label">La Ola</div>
      <div class="bubble">Bonjorno! 👋🌊<br>Ocean in sight. Music on all night.<br><br>What can I help you with today?</div>
    </div>
  </div>

  <div class="quick-wrap" id="quickWrap">
    <button class="q-btn" onclick="quickSend('menu')">🍽️ Menu</button>
    <button class="q-btn" onclick="quickSend('events this week')">🎶 Events</button>
    <button class="q-btn" onclick="quickSend('location')">📍 Location</button>
    <button class="q-btn" onclick="quickSend('reserve')">📅 Reserve</button>
  </div>

  <div class="input-area">
    <div class="input-row">
      <input id="inp" placeholder="Ask anything..." onkeypress="if(event.key==='Enter')send()">
      <button class="send" onclick="send()">➤</button>
    </div>
  </div>
</div>

<script>
  const chat = document.getElementById("chat");
  const quickWrap = document.getElementById("quickWrap");

  function addMsg(text, who) {
    const d = document.createElement("div");
    d.className = "msg " + who;
    d.innerHTML = `<div class="label">${who === "bot" ? "La Ola" : "You"}</div><div class="bubble">${text}</div>`;
    chat.appendChild(d);
    chat.scrollTop = chat.scrollHeight;
  }

  function showTyping() {
    const d = document.createElement("div");
    d.className = "msg bot"; d.id = "typing";
    d.innerHTML = `<div class="label">La Ola</div><div class="typing-bubble"><span></span><span></span><span></span></div>`;
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
    inp.value = "";
    showTyping();
    const res = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });
    const data = await res.json();
    hideTyping();
    addMsg(data.reply, "bot");
  }

  function quickSend(text) {
    document.getElementById("inp").value = text;
    send();
  }
</script>

</body>
</html>
"""

@app.route(’/’)
def home():
return render_template_string(HTML_PAGE)

@app.route(’/ask’, methods=[‘POST’])
def ask():
msg = request.json.get(“message”, “”).lower()

```
# MENU
if any(x in msg for x in ["menu", "food", "eat", "drink", "manger", "boire", "prix", "price"]):
    return jsonify({"reply": "🔥 Our favourites:<br><br>🍹 Aperol Spritz — 90 DH<br>🍕 Seafood Pizza — 100 DH<br>🍤 Gambas — 90 DH<br><br>Full menu → <a href='https://linktr.ee/laolarooftop' target='_blank' style='color:#c9a96e'>linktr.ee/laolarooftop</a> 🌊<br><br>Food or drinks tonight? 😄"})

# EVENTS
if any(x in msg for x in ["event", "music", "dj", "soirée", "tonight", "week", "programme", "agenda", "concert", "party"]):
    return jsonify({"reply": "🎶 This week at La Ola:<br><br>🎵 <strong>Wunderbar Music</strong> — Thu Mar 26<br>🎸 <strong>La Brava Party</strong> — Wed Mar 25<br>🎤 <strong>Ola's Voice</strong> — Tue Mar 24<br>🎷 <strong>Sunday Jam</strong> — Every Sunday<br>🌙 <strong>Lila Gnawia</strong> — Coming soon<br><br>Full lineup → <a href='https://linktr.ee/laolarooftop' target='_blank' style='color:#c9a96e'>linktr.ee/laolarooftop</a> 👀"})

# LOCATION
if any(x in msg for x in ["location", "where", "adresse", "où", "address", "find", "map", "corniche"]):
    return jsonify({"reply": "📍 <strong>12 Bd de l'Océan Atlantique</strong><br>Ain Diab, Casablanca 🌊<br><br>Right on the corniche — ocean view included 😉<br><br>You coming tonight? 👀"})

# RESERVATION
if any(x in msg for x in ["book", "reserve", "réserver", "reservation", "table", "place"]):
    return jsonify({"reply": "Nice choice 👀<br><br>To reserve your table:<br>📩 DM us on Instagram <strong>@laolarooftop</strong><br>🔗 <a href='https://linktr.ee/laolarooftop' target='_blank' style='color:#c9a96e'>linktr.ee/laolarooftop</a><br><br>How many people are you? 😄"})

# HORAIRES
if any(x in msg for x in ["horaire", "heure", "open", "close", "hours", "quand", "when", "time"]):
    return jsonify({"reply": "🕒 We're open <strong>every day</strong><br>from <strong>09h30 to 01h00</strong> ✨<br><br>Brunch 🌅 Sunset 🌇 Late night 🌙<br>We got you covered all day long 😄"})

# COMMUNITY
if any(x in msg for x in ["family", "community", "communauté", "membre", "group"]):
    return jsonify({"reply": "❤️ Join the <strong>LA OLA FAMILY</strong> — 656 members strong!<br><br>Follow us → <strong>@laolarooftop</strong><br>🔗 <a href='https://linktr.ee/laolarooftop' target='_blank' style='color:#c9a96e'>linktr.ee/laolarooftop</a>"})

# INSTAGRAM
if any(x in msg for x in ["instagram", "insta", "follow", "social"]):
    return jsonify({"reply": "Find us on Instagram 📸<br><strong>@laolarooftop</strong><br><br>🔗 <a href='https://linktr.ee/laolarooftop' target='_blank' style='color:#c9a96e'>linktr.ee/laolarooftop</a><br><br>All events, vibes & updates are there 🌊"})

# DEFAULT
return jsonify({"reply": "Hey 👋 I can help with:<br><br>🍽️ Menu & prices<br>🎶 Events this week<br>📍 Location<br>📅 Reservations<br>🕒 Opening hours<br><br>What are you looking for? 😄"})
```

if **name** == “**main**”:
port = int(os.environ.get(“PORT”, 5000))
app.run(host=“0.0.0.0”, port=port, debug=False)