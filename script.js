document.addEventListener("DOMContentLoaded", function () {
    const chatForm = document.getElementById("chatForm");
    const chatInput = document.getElementById("chatInput");
    const chatHistory = document.getElementById("chatHistory");

    chatForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const userMessage = chatInput.value.trim();
        if (!userMessage) return;

        // Show user message with emoji
        const userDiv = document.createElement("div");
        userDiv.className = "userMessage";
        userDiv.textContent = "🧑 You: " + userMessage;
        chatHistory.appendChild(userDiv);

        chatInput.value = "";

        // Send to Flask backend
        fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: "message=" + encodeURIComponent(userMessage)
        })
        .then(response => response.json())
        .then(data => {
            const botDiv = document.createElement("div");
            botDiv.className = "botMessage";
            botDiv.innerHTML = "🤖 SME: " + data.response.replace(/\n/g, "<br>");
            chatHistory.appendChild(botDiv);

            // Scroll to bottom
            chatHistory.scrollTop = chatHistory.scrollHeight;
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });
});
