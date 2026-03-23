import os
from flask import Flask, request, jsonify
from groq import Groq
from dotenv import load_dotenv

# 1. CHARGEMENT DES VARIABLES (.env en local, Dashboard en prod)
load_dotenv()

app = Flask(__name__)

# 2. CONFIGURATION ET CONSTANTES
API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=API_KEY)

CONTACT = "05 22 79 78 85"
ADRESSE = "📍 Ain Diab, Casablanca"

# 3. INTERFACE HTML (Design Luxury & Responsive)
HTML_PAGE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>La Ola Assistant</title>
    <style>
        body { font-family: 'Inter', -apple-system, sans-serif; background:#0f172a; color:white; margin:0; }
        .chat { max-width:500px; margin:auto; height:100vh; display:flex; flex-direction:column; background:#1e293b; }
        .header { padding:20px; text-align:center; background:#020617; border-bottom: 2px solid #38bdf8; }
        .header h1 { margin:0; font-size:1.2rem; color:#38bdf8; text-transform: uppercase; letter-spacing: 2px; }
        .messages { flex:1; overflow-y:auto; padding:20px; display:flex; flex-direction:column; }
        .msg { padding:14px; border-radius:15px; margin:8px 0; max-width:85%; line-height:1.4; font-size: 0.95rem; }
        .bot { background:#334155; align-self: flex-start; border-bottom-left-radius: 2px; }
        .user { background:#38bdf8; color:black; align-self: flex-end; border-bottom-right-radius: 2px; font-weight:600; }
        .input-box { display:flex; padding:15px; background:#020617; gap:10px; }
        input { flex:1; padding:12px 18px; border-radius:25px; border:none; background:#1e293b; color:white; outline:none; }
        button { width:45px; height:45px; border-radius:50%; border:none; background:#38bdf8; cursor:pointer; font-weight:bold; }
    </style>
</head>
<body>
    <div class="chat">
        <div class="header"><h1>LA OLA ROOFTOP</h1></div>
        <div class="messages" id="chat">
            <div class="msg bot">Hey 👋 Bienvenue à La Ola 🌊<br><br>Tu veux le menu, réserver une table ou checker la vibe ?</div>
        </div>
        <div class="input-box">
            <input id="input" placeholder="Écris ici..." onkeypress="if(event.key==='Enter')send()">
            <button onclick="send()">→</button>
        </div>
    </div>
    <script>
        async function send(){
            const input = document.getElementById("input");
            const chat = document.getElementById("chat");
            const text = input.value.trim();
            if(!text) return;
            chat.innerHTML += `<div class="msg user">${text}</div>`;
            input.value = "";
            chat.scrollTop = chat.scrollHeight;
            try {
                const res = await fetch("/ask", {
                    method:"POST",
                    headers: {"Content-Type":"application/json"},
                    body: JSON.stringify({message:text})
                });
                const data = await res.json();
                chat.innerHTML += `<div class="msg bot">${data.reply}</div>`;
            } catch {
                chat.innerHTML += `<div class="msg bot">Petit souci de réseau 😅</div>`;
            }
            chat.scrollTop = chat.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return HTML_PAGE

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    msg = data.get("message", "").lower()

    # --- 1. RÉPONSES PRIORITAIRES (BUSINESS & CONVERSION) ---

    # Menu & Prix
    if any(x in msg for x in ["menu", "carte", "prix", "manger"]):
        return jsonify({
            "reply": f"Voilà quelques best sellers 🔥<br><br>🍤 Gambas<br>🍕 Seafood Pizza<br>🥗 Caesar Salad<br>🍹 Aperol Spritz<br><br>Tu veux que je te conseille selon ton mood ? 😄<br><br>📞 Réserve au {CONTACT} 😉"
        })

    # Contact & Réservation
    if any(x in msg for x in ["contact", "telephone", "numero", "appeler", "reservation", "reserver", "table"]):
        return jsonify({
            "reply": f"Pour réserver 👇<br><br>📞 <b>{CONTACT}</b><br><br>Viens directement, surtout en soirée l’ambiance est 🔥 !<br><br>📍 {ADRESSE}"
        })

    # Ambiance
    if any(x in msg for x in ["ambiance", "music", "soirée", "dj", "vibe"]):
        return jsonify({
            "reply": f"Ambiance rooftop face à l’océan 🌊<br>DJ sets, cocktails et sunset vibes 🔥<br>Parfait pour chill ou faire la fête !<br><br>📞 Réserve au {CONTACT} 😉"
        })

    # --- 2. IA (POUR LE RESTE) ---
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": f"""Tu es un serveur réel de La Ola Rooftop à Casablanca.
                    STYLE : Très court (1-2 phrases max), naturel, humain, chill.
                    INTERDIT : Phrases longues, explications inutiles, dire que tu es une IA.
                    OBJECTIF : Répondre vite, donner envie de venir, pousser à appeler.
                    INFOS : {ADRESSE}, Tel: {CONTACT}."""
                },