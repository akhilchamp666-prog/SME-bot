from flask import Flask, request, render_template_string
from Script import load_updates, search_updates

app = Flask(__name__)
df = load_updates("updates.xlsx")

# -------------------------
# Embed HTML template directly
# -------------------------
HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>SME Bot</title>
    <style>
        body { font-family: Arial, sans-serif; background-color:#f0f0f0; padding:20px; }
        h1 { text-align:center; color:#333; }
        #chat-container { width: 60%; margin: auto; background:white; border:1px solid #ccc; padding:15px; border-radius:10px; }
        #chat { border:1px solid #ccc; padding:10px; height:400px; overflow-y:scroll; background:#fafafa; }
        .user { color: blue; margin:5px 0; }
        .bot { color: green; margin:5px 0; }
        #input-container { margin-top:10px; display:flex; }
        #message { flex:1; padding:8px; font-size:14px; }
    </style>
</head>
<body>
    <h1>SME Bot</h1>
    <div id="chat-container">
        <div id="chat"></div>
        <div id="input-container">
            <input type="text" id="message" placeholder="Type here..." autofocus>
        </div>
    </div>
    <script>
        function appendMessage(sender, text){
            const chat = document.getElementById('chat');
            chat.innerHTML += '<div class="'+sender+'"><b>'+sender+':</b> '+text+'</div>';
            chat.scrollTop = chat.scrollHeight;
        }

        function sendMessage(){
            const input = document.getElementById('message');
            const msg = input.value.trim();
            if(!msg) return;
            appendMessage('You', msg);
            fetch('/chat', {
                method:'POST',
                headers:{'Content-Type':'application/x-www-form-urlencoded'},
                body:'message='+encodeURIComponent(msg)
            }).then(res=>res.text())
              .then(data=>appendMessage('SME', data));
            input.value='';
        }

        document.getElementById('message').addEventListener("keypress", function(e){
            if(e.key === "Enter"){ sendMessage(); }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['message'].strip()
    results = search_updates(df, user_input)

    if results == "greeting":
        return "Hello! How can I help you today? 🤖"

    if not results:
        return "Sorry, I cannot assist on this. Please reach out to my boss Akhil. 🤖"

    messages = [f"Update {i+1}: '{row['Description']}' — Status: {row['Status']}'"
                for i, row in enumerate(results)]
    return "<br>".join(messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
