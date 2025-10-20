from flask import Flask, request, render_template_string
import pandas as pd
import re

# -------------------------
# Flask app setup
# -------------------------
app = Flask(__name__)

# -------------------------
# Load Excel updates
# -------------------------
FILE_PATH = "updates.xlsx"

def load_updates(file_path):
    df = pd.read_excel(file_path, engine="openpyxl")
    df.columns = df.columns.str.strip().str.replace('\xa0','')
    df['Update_ID_str'] = df['Update_ID'].astype(str).str.lower()
    df['Description_str'] = df['Description'].astype(str).str.lower()
    df['Status'] = df['Status'].fillna("Active")
    return df

df = load_updates(FILE_PATH)

# -------------------------
# Stopwords and greetings
# -------------------------
STOPWORDS = {'what', 'is', 'the', 'on', 'please', 'give', 'me', 'update', 'of', 'for',
             'can', 'be', 'with', 'a', 'how', 'i', 'you', 'we', 'are', 'my', 'do',
             'billed', 'are', 'updates'}

GREETINGS = {'hi', 'hello', 'hey', 'goodmorning', 'goodafternoon'}

# -------------------------
# HTML template with chat styling
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
        .message { margin:5px 0; padding:8px 12px; border-radius:10px; max-width:70%; clear:both; }
        .user { background:#d1e7ff; float:left; text-align:left; }
        .bot { background:#d4ffd1; float:right; text-align:right; }
        #input-container { margin-top:10px; display:flex; }
        #message { flex:1; padding:8px; font-size:14px; }
        #send-btn { padding:8px 12px; margin-left:5px; font-size:14px; cursor:pointer; }
    </style>
</head>
<body>
    <h1>SME Bot</h1>
    <div id="chat-container">
        <div id="chat"></div>
        <div id="input-container">
            <input type="text" id="message" placeholder="Type here..." autofocus>
            <button id="send-btn" onclick="sendMessage()">Send</button>
        </div>
    </div>
    <script>
        function appendMessage(sender, text){
            const chat = document.getElementById('chat');
            const msgDiv = document.createElement('div');
            msgDiv.className = 'message ' + sender.toLowerCase();
            msgDiv.innerHTML = '<b>' + sender + ':</b> ' + text;
            chat.appendChild(msgDiv);
            chat.scrollTop = chat.scrollHeight;
        }

        function sendMessage(){
            const input = document.getElementById('message');
            const msg = input.value.trim();
            if(!msg) return;
            appendMessage('User', msg);
            fetch('/chat', {
                method:'POST',
                headers:{'Content-Type':'application/x-www-form-urlencoded'},
                body:'message='+encodeURIComponent(msg)
            }).then(res=>res.text())
              .then(data=>appendMessage('Bot', data));
            input.value='';
        }

        document.getElementById('message').addEventListener("keypress", function(e){
            if(e.key === "Enter"){ sendMessage(); }
        });
    </script>
</body>
</html>
"""

# -------------------------
# Flask routes
# -------------------------
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['message'].strip()
    user_input_clean = re.sub(r'[^\w\s]', '', user_input.lower())
    user_words = [w for w in user_input_clean.split() if w not in STOPWORDS]

    # Greeting detection
    if any(word in GREETINGS for word in user_words):
        return "Hello! How can I help you today? 🤖"

    # Extract numbers (Update_ID)
    numbers = re.findall(r'\d+', user_input_clean)

    # Fallback if nothing found
    if not numbers and not user_words:
        return "Sorry, I cannot assist on this. Please reach out to my boss Akhil. 🤖"

    # Search updates
    result_rows = []
    for _, row in df.iterrows():
        update_id_match = str(row['Update_ID']).lower() in numbers if numbers else True
        description_words = re.findall(r'\w+', row['Description_str'])
        keyword_match = all(kw in description_words for kw in user_words) if user_words else True

        if update_id_match and keyword_match:
            result_rows.append(row)

    if not result_rows:
        return "Sorry, I cannot assist on this. Please reach out to my boss Akhil. 🤖"
    else:
        messages = [f"Update {i+1}: '{row['Description']}' — Status: {row['Status']}" 
                    for i, row in enumerate(result_rows)]
        return "<br>".join(messages)

# -------------------------
# Run the app
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

