import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

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
    cursor: pointer;
}

.quick {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 10px;
}

.quick button {
    background: #1e293b;
    border: none;
    color: white;
    padding: 8px 12px;
    border-radius: 8px;
}
</style>
</head>

<body>
<div class="chat">
    <div class="messages" id="chat">

        <div class="msg bot">
        Welcome to La Ola 🌊<br><br>
        What are you looking for?<br><br>

        <div class="quick">
            <button onclick="quickMsg('menu')">Menu 🍽️</button>
            <button onclick="quickMsg('book')">Book a table 📅</button>
            <button onclick="quickMsg('location')">Location 📍</button>
            <button onclick="quickMsg('events')">Events 🎶</button>
        </div>
        </div>

    </div>

    <div class="input">
        <input id="input" placeholder="Ask anything..." onkeypress="if(event.key==='Enter')send()">
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

function quickMsg(text){
    document.getElementById("input").value = text;
    send();
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
    if "menu" in msg:
        return jsonify({
            "reply": """Here’s what people love 🔥<br><br>
🍹 Aperol Spritz — 90 DH<br>
🍕 Seafood Pizza — 100 DH<br>
🍤 Gambas — 90 DH<br><br>
You coming for food or drinks? 😄"""
        })

    # LOCATION
    if any(x in msg for x in ["location", "where", "adresse"]):
        return jsonify({
            "reply": """📍 12 Boulevard de l’Océan Atlantique, Ain Diab, Casablanca 🌊<br><br>
Easy to find on the corniche 😉<br><br>
You coming tonight?"""
        })

    # BOOK
    if "book" in msg or "reserve" in msg:
        return jsonify({
            "reply": """Nice 👀<br><br>
You can reserve directly via Instagram DM @laolarooftop 📩<br><br>
Or I can guide you — how many people?"""
        })

    # EVENTS
    if "event" in msg or "music" in msg:
        return jsonify({
            "reply": """We usually have DJ sets & a great vibe at night 🎶🔥<br><br>
Best time is after 8pm 👀<br><br>
You more chill or party?"""
        })

    # DEFAULT
    return jsonify({
        "reply": """Hey 👋<br><br>
I can help with:<br>
• Menu 🍽️<br>
• Booking 📅<br>
• Location 📍<br>
• Events 🎶<br><br>
What do you need? 😄"""
    })

if __name__ == "__main__":
    app.run(debug=True)