document.addEventListener('DOMContentLoaded', function() {
    function handleChat(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        let messagesEl, inputEl, sendBtn, quickActionsEl;

        if (containerId === 'chatbot-container') {
            // Selectors for the main chatbot page
            messagesEl = document.getElementById('chatbotMessages');
            inputEl = document.getElementById('chatInput');
            sendBtn = document.getElementById('chatSendBtn');
            quickActionsEl = null; // No quick actions on the main page
        } else if (containerId === 'chatbot-rectangle') {
            // Selectors for the sidebar chat on the predict page
            messagesEl = document.getElementById('chatbotMessagesRect');
            inputEl = document.getElementById('chatInputRect');
            sendBtn = document.getElementById('chatSendBtnRect');
            quickActionsEl = document.getElementById('quickActionsRect');
        } else {
            return; // Exit if the container ID is not recognized
        }

        // Ensure all required elements are present
        if (!messagesEl || !inputEl || !sendBtn) {
            console.error(`Chat elements not found in container: ${containerId}`);
            return;
        }
        
        // Function to add a message to the chat window
        function addMessage(text, sender) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `chatbot-message ${sender}`;
            messageDiv.innerHTML = text.replace(/\n/g, '<br>');
            messagesEl.appendChild(messageDiv);
            messagesEl.scrollTop = messagesEl.scrollHeight;
        }

        // Function to render quick action buttons
        function renderQuickActions(actions = []) {
            if (!quickActionsEl) return;
            quickActionsEl.innerHTML = '';
            if (actions.length === 0) return;

            actions.forEach(action => {
                const button = document.createElement('button');
                button.className = 'quick-action-btn-rect';
                button.textContent = action.question;
                button.addEventListener('click', () => {
                    addMessage(action.question, 'user');
                    fetchChatResponse(action.prompt);
                });
                quickActionsEl.appendChild(button);
            });
        }

        // Function to fetch a response from the chatbot API
        async function fetchChatResponse(prompt) {
            const thinkingDiv = document.createElement('div');
            thinkingDiv.className = 'chatbot-message bot thinking';
            thinkingDiv.innerHTML = '<span>.</span><span>.</span><span>.</span>';
            messagesEl.appendChild(thinkingDiv);
            messagesEl.scrollTop = messagesEl.scrollHeight;

            inputEl.disabled = true;
            sendBtn.disabled = true;
            if (quickActionsEl) quickActionsEl.style.pointerEvents = 'none';

            try {
                const response = await fetch(`/chat/${encodeURIComponent(prompt)}`, { method: 'POST' });
                if (!response.ok) throw new Error('Network response was not ok.');
                
                const data = await response.json();
                
                messagesEl.removeChild(thinkingDiv);

                if (data.status === 'ok') {
                    addMessage(data.message, 'bot');
                    renderQuickActions(data.quick_actions);
                } else {
                    addMessage(data.message || 'Sorry, an error occurred.', 'bot');
                }
            } catch (error) {
                console.error('Chatbot fetch error:', error);
                if (messagesEl.contains(thinkingDiv)) {
                    messagesEl.removeChild(thinkingDiv);
                }
                addMessage('Sorry, I couldn\'t connect to the assistant right now.', 'bot');
            } finally {
                inputEl.disabled = false;
                sendBtn.disabled = false;
                if (quickActionsEl) quickActionsEl.style.pointerEvents = 'auto';
                inputEl.focus();
            }
        }

        function sendMessage() {
            const prompt = inputEl.value.trim();
            if (!prompt) return;
            addMessage(prompt, 'user');
            inputEl.value = '';
            fetchChatResponse(prompt);
        }

        sendBtn.addEventListener('click', sendMessage);
        inputEl.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
        
    }

    handleChat('chatbot-container');
    handleChat('chatbot-rectangle');
});