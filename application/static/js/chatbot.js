document.addEventListener("DOMContentLoaded", function () {
  const sendButton = document.getElementById("send-btn");
  const userInput = document.getElementById("user-input");
  const chatContent = document.getElementById("chat-content");

  sendButton.addEventListener("click", function () {
    const userMessage = userInput.value.trim();
    if (userMessage !== "") {
      appendUserMessage(userMessage);
      // Simulate bot response (replace this with actual bot logic)
      setTimeout(() => {
        const botMessage =
          "This is a bot response. Replace it with your bot logic.";
        appendBotMessage(botMessage);
      }, 500);
      userInput.value = "";
    }
  });

  function appendUserMessage(message) {
    const userDiv = document.createElement("div");
    userDiv.className = "user-message";
    userDiv.textContent = message;
    chatContent.appendChild(userDiv);
    chatContent.scrollTop = chatContent.scrollHeight;
  }

  function appendBotMessage(message) {
    const botDiv = document.createElement("div");
    botDiv.className = "bot-message";
    botDiv.textContent = message;
    chatContent.appendChild(botDiv);
    chatContent.scrollTop = chatContent.scrollHeight;
  }
});
