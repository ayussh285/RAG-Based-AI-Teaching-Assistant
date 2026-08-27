const chatArea = document.getElementById("chatArea");
const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const welcomeScreen = document.getElementById("welcomeScreen");
const newChatBtn = document.getElementById("newChatBtn");


// ============================================================
// SEND MESSAGE
// ============================================================

chatForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const query = messageInput.value.trim();

    if (!query) {
        return;
    }

    // Remove welcome screen after first question
    if (welcomeScreen) {
        welcomeScreen.remove();
    }

    // Display user message
    addMessage("user", query);

    // Clear input
    messageInput.value = "";

    // Reset textarea height
    resetTextarea();

    // Disable input while processing
    setLoading(true);

    // Show AI loading message
    const loadingMessage = addLoadingMessage();

    try {

        const response = await fetch("/ask", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                query: query
            })
        });


        const data = await response.json();


        // Remove loading message
        loadingMessage.remove();


        if (!response.ok || !data.success) {

            addErrorMessage(
                data.error || "Something went wrong."
            );

            return;
        }


        // Display AI response
        addMessage("ai", data.response);


    } catch (error) {

        console.error("Request error:", error);

        loadingMessage.remove();

        addErrorMessage(
            "Unable to connect to VidMentor backend. Make sure the Flask server is running."
        );

    } finally {

        setLoading(false);

    }

});


// ============================================================
// ADD MESSAGE
// ============================================================

function addMessage(type, text) {

    const wrapper = document.createElement("div");

    wrapper.className = "message-wrapper";


    const message = document.createElement("div");

    message.className =
        type === "user"
            ? "message user-message"
            : "message ai-message";


    // Avatar
    const avatar = document.createElement("div");

    avatar.className = "message-avatar";

    avatar.textContent =
        type === "user"
            ? "U"
            : "🤖";


    // Content
    const content = document.createElement("div");

    content.className = "message-content";


    // Name
    const name = document.createElement("div");

    name.className = "message-name";

    name.textContent =
        type === "user"
            ? "You"
            : "VidMentor";


    // Text
    const messageText = document.createElement("div");

    messageText.className = "message-text";

    messageText.textContent = text;


    content.appendChild(name);
    content.appendChild(messageText);

    message.appendChild(avatar);
    message.appendChild(content);

    wrapper.appendChild(message);

    chatArea.appendChild(wrapper);


    scrollToBottom();

}


// ============================================================
// LOADING MESSAGE
// ============================================================

function addLoadingMessage() {

    const wrapper = document.createElement("div");

    wrapper.className = "message-wrapper";


    const message = document.createElement("div");

    message.className = "message ai-message";


    const avatar = document.createElement("div");

    avatar.className = "message-avatar";

    avatar.textContent = "🤖";


    const content = document.createElement("div");

    content.className = "message-content";


    const name = document.createElement("div");

    name.className = "message-name";

    name.textContent = "VidMentor";


    const indicator = document.createElement("div");

    indicator.className = "typing-indicator";


    for (let i = 0; i < 3; i++) {

        const dot = document.createElement("span");

        indicator.appendChild(dot);

    }


    content.appendChild(name);
    content.appendChild(indicator);

    message.appendChild(avatar);
    message.appendChild(content);

    wrapper.appendChild(message);

    chatArea.appendChild(wrapper);


    scrollToBottom();


    return wrapper;

}


// ============================================================
// ERROR MESSAGE
// ============================================================

function addErrorMessage(text) {

    const wrapper = document.createElement("div");

    wrapper.className = "message-wrapper";


    const message = document.createElement("div");

    message.className = "message ai-message";


    const avatar = document.createElement("div");

    avatar.className = "message-avatar";

    avatar.textContent = "⚠️";


    const content = document.createElement("div");

    content.className = "message-content";


    const error = document.createElement("div");

    error.className = "error-message";

    error.textContent = text;


    content.appendChild(error);

    message.appendChild(avatar);
    message.appendChild(content);

    wrapper.appendChild(message);

    chatArea.appendChild(wrapper);


    scrollToBottom();

}


// ============================================================
// LOADING STATE
// ============================================================

function setLoading(isLoading) {

    sendBtn.disabled = isLoading;

    messageInput.disabled = isLoading;


    if (isLoading) {

        sendBtn.style.opacity = "0.5";

    } else {

        sendBtn.style.opacity = "1";

        messageInput.focus();

    }

}


// ============================================================
// AUTO RESIZE TEXTAREA
// ============================================================

messageInput.addEventListener("input", function () {

    this.style.height = "auto";

    this.style.height =
        Math.min(this.scrollHeight, 150) + "px";

});


// ============================================================
// ENTER TO SEND
// SHIFT + ENTER = NEW LINE
// ============================================================

messageInput.addEventListener("keydown", function (event) {

    if (
        event.key === "Enter" &&
        !event.shiftKey
    ) {

        event.preventDefault();

        chatForm.requestSubmit();

    }

});


// ============================================================
// SUGGESTION BUTTONS
// ============================================================

document.querySelectorAll(".suggestion").forEach(
    function (button) {

        button.addEventListener("click", function () {

            const question =
                this.dataset.question;

            messageInput.value = question;

            messageInput.dispatchEvent(
                new Event("input")
            );

            chatForm.requestSubmit();

        });

    }
);


// ============================================================
// NEW CHAT
// ============================================================

newChatBtn.addEventListener("click", function () {

    location.reload();

});


// ============================================================
// RESET TEXTAREA
// ============================================================

function resetTextarea() {

    messageInput.style.height = "auto";

}


// ============================================================
// SCROLL TO BOTTOM
// ============================================================

function scrollToBottom() {

    setTimeout(function () {

        chatArea.scrollTo({
            top: chatArea.scrollHeight,
            behavior: "smooth"
        });

    }, 50);

}