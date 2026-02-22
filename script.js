const API_URL = "https://YOUR_BACKEND_URL"; // Replace with backend
const SECRET = "YOUR_SECRET_KEY";

const startBtn = document.getElementById("start");
const endBtn = document.getElementById("end");
const status = document.getElementById("status");
const usernameInput = document.getElementById("username");

async function postShift(endpoint) {
    const username = usernameInput.value.trim();
    if (!username) { status.textContent = "Enter your name!"; return; }

    try {
        const res = await fetch(`${API_URL}/shift/${endpoint}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, secret: SECRET })
        });
        const data = await res.json();
        status.textContent = data.status === "success" ? `${endpoint.toUpperCase()} successful!` : data.message;
    } catch (e) {
        status.textContent = "Error connecting to backend";
    }
}

startBtn.addEventListener("click", () => postShift("start"));
endBtn.addEventListener("click", () => postShift("end"));

// Auto-end shift on tab close
window.addEventListener("beforeunload", async (e) => {
    const username = usernameInput.value.trim();
    if (!username) return;
    navigator.sendBeacon(`${API_URL}/shift/end`, JSON.stringify({ username, secret: SECRET }));
});
