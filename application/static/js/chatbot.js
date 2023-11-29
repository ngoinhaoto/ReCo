document.addEventListener("DOMContentLoaded", function () {
  const chatBox = document.getElementById("chat");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");

  sendBtn.addEventListener("click", function () {
    const userMessage = userInput.value.trim();

    if (userMessage !== "") {
      // Display user message
      displayMessage(userMessage, "user-message");

      // Simulate bot response (replace this with actual backend logic)
      setTimeout(function () {
        const botResponse = 'This is a bot response to "' + userMessage + '"';
        displayMessage(botResponse, "bot-message");
      }, 500); // Simulating bot response delay
    }

    userInput.value = ""; // Clear user input
  });

  function displayMessage(message, type) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add(type);
    messageDiv.innerHTML = `<p>${message}</p>`;
    chatBox.appendChild(messageDiv);

    // Scroll to bottom of chat box
    chatBox.scrollTop = chatBox.scrollHeight;
  }
});
