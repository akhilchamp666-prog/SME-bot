from flask import Flask, request, render_template
from Script import load_updates, search_updates

app = Flask(__name__)
df = load_updates("updates.xlsx")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['message'].strip()
    results = search_updates(df, user_input)

    if results == "greeting":
        return "Hello! How can I help you today? 🤖"

    if not results:
        return "Sorry, I cannot assist on this. Please reach out to my boss Akhil. 🤖"

    messages = [f"Update {i+1}: '{row['Description']}' — Status: {row['Status']}" 
                for i, row in enumerate(results)]
    return "<br>".join(messages)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
