
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-message");
    document.addEventListener("DOMContentLoaded", function () {
    const sendBtn = document.getElementById("send-btn");
    const welcomeBox = document.getElementById("welcome-box");
    const conversationsList = document.getElementById("conversations-list");
    const newConversationBtn = document.getElementById("new-conversation");

    let currentConversation = []; // Mantener el historial en frontend
    let conversationId = null;
    let conversationName = "Nueva conversación";
    let botReceivedMessage = false;

    const guardarConversaciones = true;  // Cambia a false si NO quieres guardar

    function showTypingIndicator() {
        removeTypingIndicator();
        const typingIndicator = document.createElement("div");
        typingIndicator.classList.add("typing-indicator");
        typingIndicator.textContent = "Escribiendo...";
        chatBox.appendChild(typingIndicator);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function removeTypingIndicator() {
        const typingIndicator = document.querySelector(".typing-indicator");
        if (typingIndicator) typingIndicator.remove();
    }

    function sendMessage() {
        const userMessage = userInput.value.trim();
        if (userMessage === "") return;
        if (!conversationId) {
            startNewConversation();
        }

        appendMessage(userMessage, "user-message");
        currentConversation.push({ sender: "user", text: userMessage });
        showTypingIndicator();
        
        function appendMessage(text, className) {
            let messageDiv = document.createElement("div");
            messageDiv.classList.add("message", className);
            messageDiv.innerHTML = text.replace(/\n/g, "<br>");
            chatBox.appendChild(messageDiv);
            chatBox.scrollTop = chatBox.scrollHeight;

            // Renderizar fórmulas con MathJax
            if (window.MathJax) {
                MathJax.typesetPromise([messageDiv]).catch((err) => console.error(err.message));
            }
        }

        
        // Enviar el historial completo de la conversación junto con el nuevo mensaje
        fetch("https://armas-cq2z.onrender.com/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: userMessage,
                conversationHistory: getConversationHistory() // Obtener el historial guardado
            })
        })
        .then((response) => response.json())
        .then((data) => {
            removeTypingIndicator();
            appendMessage(data.response, "bot-message");
            currentConversation.push({ sender: "bot", text: data.response });
            welcomeBox.style.display = "none";
            botReceivedMessage = true;
            saveConversation(userMessage, data.response);  // Guardar la conversación
        })
        .catch(() => {
            removeTypingIndicator();
            appendMessage("Hubo un error. Intenta nuevamente.", "bot-message");
        });

        userInput.value = "";
    }

    // Guardar el mensaje del usuario y la respuesta del bot
    function saveConversation(userMessage, botResponse) {
        let conversationHistory = getConversationHistory();

        // Agregar el nuevo mensaje y la respuesta al historial
        conversationHistory.push({ role: "user", content: userMessage });
        conversationHistory.push({ role: "bot", content: botResponse });

        // Guardar el historial actualizado en localStorage
        localStorage.setItem("conversationHistory", JSON.stringify(conversationHistory));
    }

    // Obtener el historial guardado
    function getConversationHistory() {
        return JSON.parse(localStorage.getItem("conversationHistory")) || [];
    }

    function appendMessage(text, className) {
        let messageDiv = document.createElement("div");
        messageDiv.classList.add("message", className);
        messageDiv.innerHTML = text.replace(/\n/g, "<br>");
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function saveConversation() {
        if (!guardarConversaciones || !conversationId) return;

        const conversationData = {
            id: conversationId,
            name: conversationName,
            messages: currentConversation
        };

        // Verificación del guardado
        console.log("Guardando conversación:", conversationData);

        localStorage.setItem(`conversation_${conversationId}`, JSON.stringify(conversationData));
    }

    function loadConversation(id) {
        const conversationData = JSON.parse(localStorage.getItem(`conversation_${id}`));
        if (!conversationData) return;

        currentConversation = conversationData.messages;
        conversationId = conversationData.id;
        conversationName = conversationData.name;
        chatBox.innerHTML = "";

        // Verificación del cargado
        console.log("Cargando conversación:", conversationData);

        currentConversation.forEach((message) => {
            appendMessage(message.text, message.sender === "user" ? "user-message" : "bot-message");
        });
    }

    function addConversationToSidebar(id, name) {
        const conversationBubble = document.createElement("div");
        conversationBubble.classList.add("conversation-bubble");
        conversationBubble.textContent = name;
        conversationBubble.dataset.id = id;
        conversationBubble.addEventListener("click", () => loadConversation(id));
        conversationsList.appendChild(conversationBubble);
    }

    function startNewConversation() {
        // Generar una ID única para cada conversación
        conversationId = `conversation_${Date.now()}`;
        conversationName = "Nueva conversación";

        if (localStorage.getItem(`conversation_${conversationId}`)) {
            loadConversation(conversationId);
        } else {
            clearChat();
            saveConversation();
            loadConversation();
        }
    }

    function clearChat() {
        chatBox.innerHTML = "";
        currentConversation = [];
    }

    newConversationBtn.addEventListener("click", startNewConversation);

    sendBtn.addEventListener("click", sendMessage);
    userInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });

    loadConversation();
});
