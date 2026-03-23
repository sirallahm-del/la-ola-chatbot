import os
from flask import Flask, request, jsonify
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(**name**)

API_KEY = os.environ.get(“GROQ_API_KEY”)
if not API_KEY:
raise ValueError(“❌ GROQ_API_KEY manquante”)

client = Groq(api_key=API_KEY)

CONTACT = “05 22 79 78 85”
ADRESSE = “Ain Diab, Casablanca”
HORAIRES = “09h30 → 01h00 tous les jours”

HTML_PAGE = “””

<!DOCTYPE html>

<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>La Ola — Assistant</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
–sand: #e8dcc8;
–ocean: #1a3a4a;
–wave: #2d6a7a;
–foam: #f5f0e8;
–gold: #c9a96e;
–text: #1a1a1a;
}

body {
font-family: ‘DM Sans’, sans-serif;
background: var(–ocean);
min-height: 100vh;
display: flex;
align-items: center;
justify-content: center;
overflow: hidden;
position: relative;
}

/* Animated ocean background */
body::before {
content: ‘’;
position: fixed;
inset: 0;
background:
radial-gradient(ellipse at 20% 80%, rgba(45,106,122,0.6) 0%, transparent 50%),
radial-gradient(ellipse at 80% 20%, rgba(201,169,110,0.15) 0%, transparent 50%),
linear-gradient(160deg, #0d2535 0%, #1a3a4a 40%, #1e4d5e 100%);
z-index: 0;
}

/* Floating wave lines */
body::after {
content: ‘’;
position: fixed;
bottom: -20px;
left: -10%;
width: 120%;
height: 200px;
background: url(“data:image/svg+xml,%3Csvg xmlns=‘http://www.w3.org/2000/svg’ viewBox=‘0 0 1440 120’%3E%3Cpath fill=‘rgba(45,106,122,0.3)’ d=‘M0,60 C360,120 720,0 1080,60 C1260,90 1380,30 1440,60 L1440,120 L0,120 Z’/%3E%3C/svg%3E”) no-repeat center;
background-size: cover;
animation: waveFloat 6s ease-in-out infinite;
z-index: 0;
}

@keyframes waveFloat {
0%, 100% { transform: translateY(0); }
50% { transform: translateY(-12px); }
}

.container {
position: relative;
z-index: 1;
width: 100%;
max-width: 420px;
height: 100vh;
display: flex;
flex-direction: column;
padding: 0;
}

/* Header */
.header {
padding: 28px 24px 20px;
text-align: center;
border-bottom: 1px solid rgba(201,169,110,0.2);
background: rgba(13,37,53,0.7);
backdrop-filter: blur(12px);
}

.logo-line {
display: flex;
align-items: center;
justify-content: center;
gap: 12px;
margin-bottom: 4px;
}

.wave-icon {
font-size: 22px;
animation: sway 3s ease-in-out infinite;
}

@keyframes sway {
0%, 100% { transform: rotate(-5deg); }
50% { transform: rotate(5deg); }
}

.brand {
font-family: ‘Cormorant Garamond’, serif;
font-size: 28px;
font-weight: 300;
letter-spacing: 0.15em;
color: var(–sand);
}

.brand span {
color: var(–gold);
font-style: italic;
}

.tagline {
font-size: 11px;
letter-spacing: 0.2em;
text-transform: uppercase;
color: rgba(232,220,200,0.5);
margin-top: 2px;
}

.status {
display: inline-flex;
align-items: center;
gap: 6px;
margin-top: 10px;
font-size: 11px;
color: rgba(232,220,200,0.6);
letter-spacing: 0.05em;
}

.status-dot {
width: 6px;
height: 6px;
border-radius: 50%;
background: #4ade80;
animation: pulse 2s infinite;
}

@keyframes pulse {
0%, 100% { opacity: 1; transform: scale(1); }
50% { opacity: 0.6; transform: scale(0.8); }
}

/* Messages */
.messages {
flex: 1;
overflow-y: auto;
padding: 20px 16px;
display: flex;
flex-direction: column;
gap: 12px;
scrollbar-width: none;
}

.messages::-webkit-scrollbar { display: none; }

.msg {
max-width: 82%;
animation: fadeSlide 0.3s ease;
}

@keyframes fadeSlide {
from { opacity: 0; transform: translateY(8px); }
to { opacity: 1; transform: translateY(0); }
}

.msg.bot {
align-self: flex-start;
}

.msg.user {
align-self: flex-end;
}

.bubble {
padding: 12px 16px;
border-radius: 18px;
font-size: 14px;
line-height: 1.55;
}

.msg.bot .bubble {
background: rgba(232,220,200,0.1);
border: 1px solid rgba(201,169,110,0.2);
color: var(–sand);
border-radius: 4px 18px 18px 18px;
backdrop-filter: blur(8px);
}

.msg.user .bubble {
background: linear-gradient(135deg, var(–gold), #b8924a);
color: #1a1a1a;
border-radius: 18px 18px 4px 18px;
font-weight: 500;
}

.msg-label {
font-size: 10px;
letter-spacing: 0.08em;
text-transform: uppercase;
margin-bottom: 5px;
color: rgba(201,169,110,0.6);
}

.msg.user .msg-label {
text-align: right;
color: rgba(232,220,200,0.4);
}

/* Quick replies */
.quick-replies {
display: flex;
flex-wrap: wrap;
gap: 8px;
padding: 0 16px 12px;
}

.quick-btn {
padding: 7px 14px;
border: 1px solid rgba(201,169,110,0.35);
border-radius: 20px;
background: rgba(201,169,110,0.08);
color: var(–gold);
font-size: 12px;
font-family: ‘DM Sans’, sans-serif;
cursor: pointer;
transition: all 0.2s;
letter-spacing: 0.03em;
}

.quick-btn:hover {
background: rgba(201,169,110,0.2);
border-color: var(–gold);
}

/* Input */
.input-area {
padding: 12px 16px 20px;
background: rgba(13,37,53,0.8);
backdrop-filter: blur(12px);
border-top: 1px solid rgba(201,169,110,0.15);
}

.input-row {
display: flex;
gap: 10px;
align-items: center;
background: rgba(232,220,200,0.07);
border: 1px solid rgba(201,169,110,0.25);
border-radius: 28px;
padding: 4px 4px 4px 16px;
transition: border-color 0.2s;
}

.input-row:focus-within {
border-color: rgba(201,169,110,0.5);
}

input {
flex: 1;
background: none;
border: none;
outline: none;
color: var(–sand);
font-family: ‘DM Sans’, sans-serif;
font-size: 14px;
padding: 8px 0;
}

input::placeholder { color: rgba(232,220,200,0.3); }

.send-btn {
width: 38px;
height: 38px;
border-radius: 50%;
border: none;
background: linear-gradient(135deg, var(–gold), #b8924a);
color: #1a1a1a;
font-size: 16px;
cursor: pointer;
display: flex;
align-items: center;
justify-content: center;
transition: transform 0.15s, opacity 0.15s;
flex-shrink: 0;
}

.send-btn:hover { transform: scale(1.08); }
.send-btn:active { transform: scale(0.95); opacity: 0.8; }

/* Typing indicator */
.typing {
display: flex;
gap: 4px;
align-items: center;
padding: 12px 16px;
background: rgba(232,220,200,0.08);
border: 1px solid rgba(201,169,110,0.15);
border-radius: 4px 18px 18px 18px;
width: fit-content;
}

.typing span {
width: 6px;
height: 6px;
border-radius: 50%;
background: var(–gold);
animation: bounce 1.2s infinite;
}

.typing span:nth-child(2) { animation-delay: 0.2s; }
.typing span:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
30% { transform: translateY(-6px); opacity: 1; }
}
</style>

</head>
<body>

<div class="container">
  <div class="header">
    <div class="logo-line">
      <span class="wave-icon">🌊</span>
      <div class="brand">La <span>Ola</span></div>
      <span class="wave-icon">🌊</span>
    </div>
    <div class="tagline">Rooftop · Casablanca</div>
    <div class="status">
      <span class="status-dot"></span>
      Assistant disponible 24h/24
    </div>
  </div>

  <div class="messages" id="chat">
    <div class="msg bot">
      <div class="msg-label">La Ola</div>
      <div class="bubble">Bonjorno! 👋🌊<br>Bienvenue à La Ola Rooftop.<br>Comment je peux t'aider aujourd'hui ?</div>
    </div>
  </div>

  <div class="quick-replies" id="quickReplies">
    <button class="quick-btn" onclick="sendQuick('Menu & prix')">🍽️ Menu</button>
    <button class="quick-btn" onclick="sendQuick('Horaires')">🕒 Horaires</button>
    <button class="quick-btn" onclick="sendQuick('Réservation')">📞 Réserver</button>
    <button class="quick-btn" onclick="sendQuick('Où êtes-vous ?')">📍 Adresse</button>
  </div>

  <div class="input-area">
    <div class="input-row">
      <input id="input" placeholder="Écris ton message..." onkeypress="if(event.key==='Enter')send()">
      <button class="send-btn" onclick="send()">➤</button>
    </div>
  </div>
</div>

<script>
  const chat = document.getElementById("chat");
  const quickReplies = document.getElementById("quickReplies");

  function addMsg(text, who) {
    const div = document.createElement("div");
    div.className = `msg ${who}`;
    div.innerHTML = `
      <div class="msg-label">${who === 'bot' ? 'La Ola' : 'Vous'}</div>
      <div class="bubble">${text}</div>
    `;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
  }

  function showTyping() {
    const div = document.createElement("div");
    div.className = "msg bot";
    div.id = "typing";
    div.innerHTML = `
      <div class="msg-label">La Ola</div>
      <div class="typing"><span></span><span></span><span></span></div>
    `;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
  }

  function hideTyping() {
    const t = document.getElementById("typing");
    if (t) t.remove();
  }

  async function send() {
    const input = document.getElementById("input");
    const text = input.value.trim();
    if (!text) return;

    quickReplies.style.display = "none";
    addMsg(text, "user");
    input.value = "";
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

  function sendQuick(text) {
    document.getElementById("input").value = text;
    send();
  }
</script>

</body>
</html>
"""

@app.route(”/”)
def home():
return HTML_PAGE

@app.route(”/ask”, methods=[“POST”])
def ask():
data = request.get_json()
msg = data.get(“message”, “”).lower()

```
if any(x in msg for x in ["horaire", "heure", "ouvert", "ferme", "quand"]):
    return jsonify({"reply": f"🕒 On t'accueille <strong>tous les jours de {HORAIRES}</strong> ✨<br><br>Tu prévois de venir pour le déj ou le coucher de soleil ? 🌅"})

if any(x in msg for x in ["menu", "carte", "prix", "manger", "boire", "food"]):
    return jsonify({"reply": "🍹 <strong>Nos incontournables :</strong><br>• Aperol Spritz<br>• Seafood Pizza<br>• Gambas grillées<br>• Cocktails signature<br><br>Tu veux qu'on te réserve une table ? 😄"})

if any(x in msg for x in ["contact", "numero", "réservation", "reserver", "réserver", "résa", "book"]):
    return jsonify({"reply": f"📞 Appelle-nous au <strong>{CONTACT}</strong><br>📍 {ADRESSE}<br><br>On s'occupe de tout pour toi 🌊"})

if any(x in msg for x in ["où", "adresse", "localisation", "situé", "trouver", "corniche", "ain diab"]):
    return jsonify({"reply": f"📍 On est sur la <strong>Corniche d'Ain Diab, Casablanca</strong> 🌊<br><br>Face à l'océan, tu peux pas nous rater 😉<br>Pour plus de détails : <strong>{CONTACT}</strong>"})

if any(x in msg for x in ["ambiance", "soirée", "dj", "musique", "vibe", "event"]):
    return jsonify({"reply": "🔥 Rooftop + océan + DJ = vibe incomparable 🌅<br><br>Check notre Instagram <strong>@laolarooftop</strong> pour les events à venir 👀"})

try:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": f"""Tu es l'assistant de La Ola Rooftop à Casablanca.
```

Réponds TOUJOURS comme ça :

- Maximum 2-3 phrases courtes
- Ton chill, fun et chaleureux
- Utilise des emojis avec modération
- Donne toujours envie de venir
- Ne dis JAMAIS “je ne sais pas” ou “consultez Instagram” pour les infos de base

Infos :

- Adresse : {ADRESSE}
- Horaires : {HORAIRES}
- Contact : {CONTACT}
- On est un rooftop avec vue sur l’océan Atlantique
  “””
  },
  {“role”: “user”, “content”: msg}
  ]
  )
  reply = response.choices[0].message.content[:200]
  return jsonify({“reply”: reply})
  
  except Exception:
  return jsonify({“reply”: f”Petit souci technique 😅<br>Appelle-nous directement au <strong>{CONTACT}</strong> 📞”})

if **name** == “**main**”:
port = int(os.environ.get(“PORT”, 5000))
app.run(host=“0.0.0.0”, port=port, debug=False)