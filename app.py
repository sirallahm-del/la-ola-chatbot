import os
from flask import Flask, render_template_string, request, jsonify
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# INFOS
ADRESSE = "📍 12 Boulevard de l’Océan Atlantique, Ain Diab, Casablanca"
HORAIRES = "🕒 Ouvert tous les jours de 09h30 à 01h00"
CONTACTS = "📞 07 67 39 31 09"

HTML_PAGE = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>La Ola AI</title>

<style>
body {
    font-family: Arial;
    background: #0f172a;
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

.bot { background: #334155; }
.user { background: #38bdf8; color: black; margin-left: auto; }

.input {
    display: flex;
    padding: 10px;
}

input {
    flex: 1;
    padding: 10px;
}

button {
    padding: 10px;
}
</style>
</head>

<body>
<div class="chat">
    <div class="messages" id="chat">
        <div class="msg bot">Hey 👋 bienvenue à La Ola 🌊  
Tu cherches le menu, les prix ou une réservation ?</div>
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

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    msg = data.get("message", "").lower()

    # MENU
    if any(x in msg for x in ["menu", "carte", "prix"]):
        return jsonify({
            "reply": """Voici quelques options 🔥<br><br>
🍹 Aperol Spritz — 90 DH<br>
🍕 Seafood Pizza — 100 DH<br>
🍤 Gambas — 90 DH<br>
🍺 Corona — 75 DH<br><br>
Tu veux plus de choix ou tu viens tester ça directement ? 😄"""
        })

    # ADRESSE
    if any(x in msg for x in ["adresse", "où", "location"]):
        return jsonify({
            "reply": f"{ADRESSE}<br><br>Facile à trouver sur la corniche 🌊 tu viens quand ?"
        })

    # HORAIRES
    if any(x in msg for x in ["horaire", "open", "heure"]):
        return jsonify({
            "reply": f"{HORAIRES}<br><br>Plutôt brunch ou soirée ? 😏"
        })

    # RÉCLAMATION
    if any(x in msg for x in ["problème", "mauvais", "serveur", "reclamation"]):
        return jsonify({
            "reply": """Ah mince désolé pour ça 🙏<br><br>
Dis-moi ce qui s’est passé ? Je peux voir ça direct avec l’équipe 👀"""
        })

    # IA
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """
Tu es le staff de La Ola Rooftop.

STYLE :
- naturel
- humain
- chill
- comme un serveur sympa

RÈGLES :
- réponses courtes
- pas de langage robot
- pas de phrases compliquées
- vibe cool 🌊

OBJECTIF :
- répondre simplement
- donner envie de venir
- proposer menu ou réservation

INFOS IMPORTANTES :
Adresse : 12 Boulevard de l’Océan Atlantique, Ain Diab, Casablanca
Horaires : 09h30 - 01h00

Tu dois toujours répondre naturellement.
"""
            },
            {"role": "user", "content": msg}
        ]
    )

    reply = response.choices[0].message.content

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)