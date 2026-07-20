const themeBtn = document.getElementById("themeBtn");
const form = document.getElementById("form");
const chat = document.getElementById("chat");
const input = document.getElementById("message");

// Theme Toggle
themeBtn.onclick = () => {
    document.body.classList.toggle("dark");
    themeBtn.textContent =
        document.body.classList.contains("dark") ? "☀️" : "🌙";
};

// Send Message
form.addEventListener("submit", async (e) => {

    e.preventDefault();

    const text = input.value.trim();

    if (!text) return;

    // User Message
    chat.innerHTML += `
        <div class="user">
            ${text}
        </div>
    `;

    input.value = "";

    chat.scrollTop = chat.scrollHeight;

    // Typing Animation
    const loading = document.createElement("div");

    loading.className = "typing";

    loading.innerHTML = `
        <span></span>
        <span></span>
        <span></span>
    `;

    chat.appendChild(loading);

    chat.scrollTop = chat.scrollHeight;

    try {

        const res = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: text
            })

        });

        const data = await res.json();

        loading.remove();

        chat.innerHTML += `
            <div class="bot">
                ${data.reply}
            </div>
        `;

    } catch (err) {

        loading.remove();

        chat.innerHTML += `
            <div class="bot">
                Something went wrong.
            </div>
        `;
    }

    chat.scrollTop = chat.scrollHeight;

});