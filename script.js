document.getElementById('send-button').addEventListener('click', sendMessage);

function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() === '') return;

    const chatThread = document.getElementById('chat-thread');
    const userMessage = document.createElement('div');
    userMessage.className = 'user-message';
    userMessage.innerText = userInput;
    chatThread.appendChild(userMessage);

    document.getElementById('user-input').value = '';

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        const architectMessage = document.createElement('div');
        architectMessage.className = 'architect-message';
        architectMessage.innerText = data.response;
        chatThread.appendChild(architectMessage);
        updateChatHistory(userInput, data.response);
    });
}

function updateChatHistory(userMessage, architectMessage) {
    const chatHistory = document.getElementById('chat-history');
    const chatItem = document.createElement('li');
    chatItem.innerText = `You: ${userMessage} - BYTE: ${architectMessage}`;
    chatHistory.appendChild(chatItem);
}
