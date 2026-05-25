// --- Theme Toggle Logic ---
const themeToggleBtn = document.getElementById('theme-toggle');
if (localStorage.getItem('theme') === 'dark') {
    document.body.classList.add('dark-mode');
    themeToggleBtn.innerText = '☀️ Light';
}

function toggleTheme() {
    document.body.classList.toggle('dark-mode');
    if (document.body.classList.contains('dark-mode')) {
        localStorage.setItem('theme', 'dark');
        themeToggleBtn.innerText = '☀️ Light';
    } else {
        localStorage.setItem('theme', 'light');
        themeToggleBtn.innerText = '🌙 Dark';
    }
}

// --- Core Application Logic ---
let myName = prompt("Welcome to the chat! Please enter your username:", "Student");
if (!myName || myName.trim() === "") {
    myName = "Anonymous";
}

const knownUsers = new Set();
const userListUI = document.getElementById("active-users-list");
function updateSidebar() {
    userListUI.innerHTML = "<li><div class='status-dot'></div> <b>" + myName + " (You)</b></li>";
    knownUsers.forEach(function(user) {
        userListUI.innerHTML += "<li><div class='status-dot'></div> " + user + "</li>";
    });
}

updateSidebar();

const socket = new WebSocket("ws://127.0.0.1:5557"); 
const chatBox = document.getElementById("chat-box");
const msgInput = document.getElementById("message-input");

msgInput.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }
});
socket.onopen = function(event) {
    chatBox.innerHTML += "<div class='message system-msg'>Successfully connected as <b>" + myName + "</b>!</div>";
    socket.send("SYSTEM_JOIN|||" + myName);
};

window.addEventListener("beforeunload", function() {
    socket.send("SYSTEM_LEAVE|||" + myName);
});
socket.onmessage = function(event) {
    const rawData = event.data;
    // 1. Admin Broadcasts
    if (rawData.startsWith("SERVER_ADMIN:")) {
        const actualMessage = rawData.replace("SERVER_ADMIN:", "");
        chatBox.innerHTML += "<div class='message system-msg' style='background: #ffeeba; color: #856404;'><b>[Admin Announcement]:</b> " + actualMessage + "</div>";
        chatBox.scrollTop = chatBox.scrollHeight; 
        return;
    }

    // 2. User Joined
    if (rawData.startsWith("SYSTEM_JOIN|||")) {
        const joinedName = rawData.replace("SYSTEM_JOIN|||", "");
        if (!knownUsers.has(joinedName) && joinedName !== myName) {
            knownUsers.add(joinedName);
            updateSidebar(); 
            chatBox.innerHTML += "<div class='message system-msg'><b>" + joinedName + "</b> joined the chat!</div>";
            chatBox.scrollTop = chatBox.scrollHeight;
            socket.send("SYSTEM_PRESENT|||" + myName);
        }
        return;
    }

    // 3. User Already Present (Roll Call)
    if (rawData.startsWith("SYSTEM_PRESENT|||")) {
        const existingUser = rawData.replace("SYSTEM_PRESENT|||", "");
        if (!knownUsers.has(existingUser) && existingUser !== myName) {
            knownUsers.add(existingUser);
            updateSidebar(); 
        }
        return;
    }

    // 4. User Left
    if (rawData.startsWith("SYSTEM_LEAVE|||")) {
        const leftName = rawData.replace("SYSTEM_LEAVE|||", "");
        if (knownUsers.has(leftName)) {
            knownUsers.delete(leftName);
            updateSidebar(); 
            chatBox.innerHTML += "<div class='message system-msg' style='background: #f8d7da; color: #721c24;'><b>" + leftName + "</b> left the chat.</div>";
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        return;
    }

    // 5. Standard Chat Message
    let senderName = "Unknown";
    let messageText = rawData;

    if (rawData.includes("|||")) {
        let parts = rawData.split("|||");
        senderName = parts[0]; 
        messageText = parts[1]; 

        if (!knownUsers.has(senderName) && senderName !== myName) {
            knownUsers.add(senderName);
            updateSidebar();
        }
    } else {
        messageText = rawData;
    }

    chatBox.innerHTML += "<div class='message friend-msg'><b>" + senderName + "</b><br>" + messageText + "</div>";
    chatBox.scrollTop = chatBox.scrollHeight; 
};

function sendMessage() {
    const text = msgInput.value.trim();
    if (text !== "") {
        socket.send(myName + "|||" + text);
        chatBox.innerHTML += "<div class='message my-msg'><b>" + myName + " (You)</b><br>" + text + "</div>";
        msgInput.value = ""; 
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}