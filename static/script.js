// Theme toggle
const toggleThemeBtn = document.getElementById('toggleTheme');
const html = document.documentElement;

let darkMode = true;
toggleThemeBtn.addEventListener('click', () => {
    darkMode = !darkMode;
    html.setAttribute('data-bs-theme', darkMode ? 'dark' : 'light');
    toggleThemeBtn.textContent = darkMode ? '🌙' : '☀️';
});

// Complaint submission
const submitBtn = document.getElementById('submitComplaint');
const complaintInput = document.getElementById('complaintInput');

submitBtn.addEventListener('click', async () => {
    const complaint = complaintInput.value.trim();
    if (!complaint) {
        alert('Please enter your complaint.');
        return;
    }
    const res = await fetch('/api/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ complaint })
    });
    const data = await res.json();
    alert(data.result);
    complaintInput.value = '';
});

// Start Submission button (placeholder)
document.getElementById('startSubmission').addEventListener('click', () => {
    alert('Voice submission coming soon!');
});
