// chatbot.js

const chatWindow = document.getElementById("chatWindow");
const chatForm = document.getElementById("chatForm");
const chatInput = document.getElementById("chatInput");

// Simple rules-based responses for FinBot
function getFinBotReply(message) {
const text = message.toLowerCase();

if (text.includes("hello") || text.includes("hi")) {
return "Hi! I’m FinBot. I can help you track expenses, understand savings, and plan budgets. Ask me anything about your personal finance.";
}

if (text.includes("budget")) {
return "To build a basic budget, list your monthly income, subtract fixed expenses (rent, EMIs, utilities), then set limits for variable spending and savings goals.";
}

if (text.includes("savings") || text.includes("save money")) {
return "A common rule is the 50-30-20 rule: 50% needs, 30% wants, 20% savings or debt repayment. You can tweak it based on your income and goals.";
}

if (text.includes("credit score")) {
return "Your credit score improves when you pay bills/EMIs on time, keep credit utilization low (ideally under 30%), and avoid frequent new loan/credit card applications.";
}

if (text.includes("investment") || text.includes("invest")) {
return "For beginners, it’s safer to start with diversified options like index funds or mutual funds instead of individual stocks, and always match investments to your risk level.";
}

if (text.includes("expense") || text.includes("spending")) {
return "Try categorizing expenses into needs, wants, and savings. Track them weekly so you can see where to cut back and stay within your budget.";
}

// Default fallback
return "I’m not sure about that yet, but you can ask me about budgeting, savings, expenses, credit score, or basic investments.";
}

// Utility to create and append a chat bubble
function appendMessage(sender, text) {
const msgDiv = document.createElement("div");
msgDiv.classList.add("cb-msg");
msgDiv.classList.add(sender === "bot" ? "cb-msg-bot" : "cb-msg-user");

const p = document.createElement("p");
p.textContent = text;

msgDiv.appendChild(p);
chatWindow.appendChild(msgDiv);
chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Handle form submit
chatForm.addEventListener("submit", function (e) {
e.preventDefault();

const message = chatInput.value.trim();
if (!message) return;

// 1. Show user message
appendMessage("user", message);

// 2. Clear input
chatInput.value = "";

// 3. Get FinBot reply and show it
const reply = getFinBotReply(message);
setTimeout(() => {
appendMessage("bot", reply);
}, 400); // small delay to feel more natural
});