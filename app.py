import os
from flask import Flask, request, jsonify
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.environ.get("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("❌ GROQ_API_KEY manquante")

client = Groq(api_key=API_KEY)

CONTACT = "05 22 79 78 85"
ADRESSE = "📍 Ain Diab, Casablanca"
HORAIRES = "🕒 09h30 → 01h00 tous les jours"

HTML_PAGE = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>La Ola Assistant</title>

<style>
body { font-family: Arial; background:#0f172a; color:white; margin:0; }
.chat { max-width:500px; margin:auto; height:100vh; display:flex; flex-direction:column; }
.messages { flex:1; overflow-y:auto; padding:20px; }
.msg { padding:12px; border-radius:12px; margin:8px 0; max-width:80%; }
.bot { background:#334155; }
.user { background:#38bdf8; color:black; margin-left:auto; }
.input { display:flex; padding:10px; }
input { flex:1; padding:10px; }
button { padding:10px; }
</style>
</head>

<body>
<div class="chat">
    <div class="messages" id="chat">
        <div class="msg bot">Hey 👋 bienvenue à La Ola 🌊<br>Menu, réservation ou ambiance ?</div>
    </div>

    <div class="input">
        <input id="input" placeholder="Écris ici..." onkeypress="if(event.key==='Enter')send()">
        <button onclick="send()">→</button>
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

    # 🔥 réponses rapides (ULTRA IMPORTANT)

    if "horaire" in msg or "heure" in msg:
        return jsonify({"reply": f"{HORAIRES} 🌊"})

    if any(x in msg for x in ["menu", "carte", "prix"]):
        return jsonify({
            "reply": f"🍹 Aperol Spritz<br>🍕 Seafood Pizza<br>🍤 Gambas<br><br>Tu veux autre chose ? 😄"
        })

    if any(x in msg for x in ["contact", "numero", "reservation", "reserver"]):
        return jsonify({
            "reply": f"📞 {CONTACT}<br>{ADRESSE}<br>Appelle-moi je te réserve 😉"
        })

    if any(x in msg for x in ["où", "localisation", "adresse"]):
        return jsonify({
            "reply": f"{ADRESSE} 📍<br>Sur la corniche, easy à trouver 😉"
        })

    if any(x in msg for x in ["ambiance", "soirée", "dj"]):
        return jsonify({
            "reply": f"Rooftop + océan 🌊 DJ + sunset 🔥<br>viens tu vas kiffer"
        })

    # 🤖 IA fallback (style humain)
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": f"""
Tu bosses à La Ola Rooftop.

Réponds comme un humain :
- très court
- naturel
- chill
- pas de texte long

Toujours donner envie de venir.

Infos :
{ADRESSE}
{CONTACT}
"""
                },
                {"role": "user", "content": msg}
            ]
        )

        reply = response.choices[0].message.content[:150]
        reply += f"<br><br>📞 {CONTACT}"

        return jsonify({"reply": reply})

    except Exception:
        return jsonify({
            "reply": f"Petit bug 😅 appelle au {CONTACT}"
        })


if __name__ == "__main__":
    app.run(debug=True)