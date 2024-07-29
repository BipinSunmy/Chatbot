document.getElementById('send-text').addEventListener('click', function() {
    const messageInput = document.getElementById('message');
    const urlInput = document.getElementById('upload-url');
    const message = messageInput.value;
    const url = urlInput.value;

    if (message.trim() === '' && url.trim() === '') {
        addMessageToChatBox('No valid input received', 'bot-message');
        return;
    }

    // Add user's message to chat box
    addMessageToChatBox(`Message: ${message} `, 'user-message');

    // Send message and URL to server
    fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `message=${encodeURIComponent(message)}&url=${encodeURIComponent(url)}`
    })
    .then(response => response.json())
    .then(data => {
        // Add bot's response to chat box
        addMessageToChatBox(`Response:${data.response}`, 'bot-message');
    })
    .catch(error => {
        console.error('Error during fetch request:', error);
        console.error('Request data:', { message, url });
        addMessageToChatBox(console.error('Error during fetch request:', error), 'bot-message');
    });
    

    // Clear input fields
    messageInput.value = '';
});

function addMessageToChatBox(message, className) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', className);
    messageDiv.textContent = message;
    chatBox.appendChild(messageDiv);

    // Scroll to the bottom of the chat box
    chatBox.scrollTop = chatBox.scrollHeight;
}
