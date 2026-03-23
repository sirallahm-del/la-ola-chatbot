import os
from flask import Flask, request, jsonify
from groq import Groq
from dotenv import load_dotenv

# Charger les variables d'env (.env en local, Render en prod)
load_dotenv()

app = Flask(__name__)

# Récupérer la clé
API_KEY = os.environ.get("GROQ_API_KEY")
print("API KEY:", API_KEY)  # utile pour logs Render

client = Groq(api_key=API_KEY)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>La Ola Chatbot</title>
<style>
body { font-family: Arial; background:#0f172a; color:white; margin:0; }
.chat { max-width:500px; margin:auto; height:100vh; display:flex; flex-direction:column; }
.messages { flex:1; overflow-y:auto; padding:20px; }
.msg { padding:12px; border-radius:12px; margin:8px 0; max-width:80%; }
.bot { background:#334155; }
.user { background:#38bdf8; color:black; margin-left:auto; }
.input { display:flex; padding:10px; background:#020617; }
input { flex:1; padding:10px; border-radius:8px; border:none; }
button { padding:10px 15px; margin-left:10px; border-radius:8px; border:none; background:#38bdf8; cursor:pointer; }
</style>
</head>
<body>

<div class="chat">
    <div class="messages" id="chat">
        <div class="msg bot">Hey 👋 bienvenue à La Ola 🌊<br>Menu, prix ou réservation ?</div>
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
    msg = data.get("message", "")

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Tu es un serveur sympa de La Ola à Casablanca."},
                {"role": "user", "content": msg}
            ]
        )
        reply = response.choices[0].message.content

    except Exception as e:
        print("ERREUR GROQ:", e)
        reply = "Erreur technique 😅"

    return jsonify({"reply": reply})