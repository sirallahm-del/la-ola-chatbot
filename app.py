import os
from flask import Flask, request, jsonify
from groq import Groq
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)

# Initialisation du client Groq
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# --- CONFIGURATION LA OLA ---
CONTACT_MANAGER = "07 67 39 31 09"
ADRESSE = "📍 12, Bd De L'Océan Atlantique, Aïn Diab, Casablanca"

HTML_PAGE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>La Ola Rooftop - Assistant</title>
    <style>
        :root { --bg: #0f172a; --card: #1e293b; --accent: #38bdf8; --text: #f8fafc; }
        body { font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); margin: 0; display: flex; justify-content: center; height: 100vh; }
        .chat-container { width: 100%; max-width: 500px; display: flex; flex-direction: column; background: var(--card); border-left: 1px solid #334155; border-right: 1px solid #334155; }
        .header { padding: 20px; background: rgba(15, 23, 42, 0.8); text-align: center; border-bottom: 1px solid #334155; }
        .header h1 { margin: 0; font-size: 1.1rem; letter-spacing: 2px; color: var(--accent); }
        #chat { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 12px; }
        .msg { padding: 12px 16px; border-radius: 15px; max-width: 85%; font-size: 0.95rem; line-height: 1.5; }
        .bot { background: #334155; align-self: flex-start; border-bottom-left-radius: 2px; }
        .user { background: var(--accent); color: #020617; align-self: flex-end; border-bottom-right-radius: 2px; font-weight: 500; }
        .menu-item { background: #0f172a; padding: 8px; border-radius: 8px; margin-top: 5px; display: flex; justify-content: space-between; border-left: 3px solid var(--accent); }
        .input-area { padding: 20px; background: #020617; display: flex; gap: 10px; }
        input { flex: 1; background: #1e293b; border: 1px solid #334155; padding: 12px; border-radius: 25px; color: white; outline: none; }
        button { background: var(--accent); border: none; width: 45px; height: 45px; border-radius: 50%; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="header"><h1>LA OLA ROOFTOP</h1></div>
        <div id="chat">
            <div class="msg bot">Bienvenue à La Ola. Je suis votre concierge virtuel. Comment puis-je vous servir ? 🌊</div>
        </div>
        <div class="input-area">
            <input id="input" placeholder="Posez votre question..." onkeypress="if(event.key==='Enter')send()">
            <button onclick="send()">→</button>
        </div>
    </div>
    <script>
        async function send(){
            const input = document.getElementById("input");
            const chat = document.getElementById("chat");
            const text = input.value.trim();
            if(!text) return;