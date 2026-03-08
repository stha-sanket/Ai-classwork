const classSelect = document.getElementById('class-select');
const subjectSelect = document.getElementById('subject-select');
const chapterSelect = document.getElementById('chapter-select');
const chatSection = document.getElementById('chat-section');
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const currentChapterTitle = document.getElementById('current-chapter-title');

// Initialize with some mock chapters
const populateChapters = () => {
    chapterSelect.innerHTML = '<option value="">Select Chapter</option>';
    for (let i = 1; i <= 30; i++) {
        const option = document.createElement('option');
        option.value = `chapter_${i}`;
        option.textContent = `Chapter ${i}: The World of Knowledge Part ${i}`;
        chapterSelect.appendChild(option);
    }
};

classSelect.addEventListener('change', () => {
    if (classSelect.value) {
        subjectSelect.disabled = false;
    } else {
        subjectSelect.disabled = true;
        chapterSelect.disabled = true;
        chatSection.style.display = 'none';
    }
});

subjectSelect.addEventListener('change', () => {
    if (subjectSelect.value) {
        chapterSelect.disabled = false;
        populateChapters();
    } else {
        chapterSelect.disabled = true;
        chatSection.style.display = 'none';
    }
});

chapterSelect.addEventListener('change', () => {
    if (chapterSelect.value) {
        chatSection.style.display = 'flex';
        currentChapterTitle.innerText = `Chatting about: ${chapterSelect.options[chapterSelect.selectedIndex].text}`;
        chatMessages.innerHTML = `
            <div class="message bot">
                Welcome to Class ${classSelect.value}, ${subjectSelect.value.charAt(0).toUpperCase() + subjectSelect.value.slice(1)}, ${chapterSelect.value.replace('_', ' ')}.
                Ask me anything from the context of this chapter!
            </div>
        `;
    } else {
        chatSection.style.display = 'none';
    }
});

const addMessage = (text, role) => {
    const div = document.createElement('div');
    div.className = `message ${role}`;
    div.innerText = text;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
};

const handleSend = async () => {
    const text = userInput.value.trim();
    if (!text) return;

    addMessage(text, 'user');
    userInput.value = '';

    // Simulate backend response or fetch from FastAPI
    // In a real RAG scenario, you'd send class, subject, and chapter IDs
    try {
        const response = await fetch('http://localhost:8000/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                class_id: classSelect.value,
                subject: subjectSelect.value,
                chapter: chapterSelect.value,
                query: text
            })
        });

        if (response.ok) {
            const data = await response.json();
            addMessage(data.response, 'bot');
        } else {
            addMessage("I'm sorry, I'm having trouble connecting to my brain! (Check if the server is running)", 'bot');
        }
    } catch (e) {
        addMessage("I'm sorry, something went wrong. Make sure you've started the backend server!", 'bot');
    }
};

sendBtn.addEventListener('click', handleSend);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSend();
});
