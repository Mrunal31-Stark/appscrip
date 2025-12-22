let currentMarkdown = "";
let currentSector = "";

async function analyzeMarket() {
    const sectorInput = document.getElementById('sectorInput');
    const apiKeyInput = document.getElementById('apiKeyInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const btnText = analyzeBtn.querySelector('.btn-text');
    const loader = analyzeBtn.querySelector('.loader');
    const statusMsg = document.getElementById('statusMessage');
    const resultContainer = document.getElementById('resultContainer');
    const reportContent = document.getElementById('reportContent');

    const sector = sectorInput.value.trim();
    const apiKey = apiKeyInput.value.trim();

    // Reset UI
    statusMsg.className = 'status hidden';
    statusMsg.innerText = '';
    resultContainer.classList.add('hidden');

    // Validation
    if (!sector) {
        showError('Please enter a target sector.');
        return;
    }
    if (!apiKey) {
        showError('Please enter the API Key.');
        return;
    }

    // Loader State
    btnText.style.opacity = '0';
    loader.style.display = 'block';
    analyzeBtn.disabled = true;

    try {
        const response = await fetch(`/analyze/${encodeURIComponent(sector)}`, {
            method: 'GET',
            headers: {
                'x-api-key': apiKey,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || 'Analysis failed');
        }

        const data = await response.json();

        currentMarkdown = data.report_markdown;
        currentSector = data.sector;

        // Render Markdown
        reportContent.innerHTML = marked.parse(currentMarkdown);
        resultContainer.classList.remove('hidden');

        // Scroll to result
        resultContainer.scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
        showError(error.message);
    } finally {
        // Reset Button
        btnText.style.opacity = '1';
        loader.style.display = 'none';
        analyzeBtn.disabled = false;
    }
}

function showError(msg) {
    const statusMsg = document.getElementById('statusMessage');
    statusMsg.innerText = msg;
    statusMsg.className = 'status error';
}

function downloadReport() {
    if (!currentMarkdown) return;

    const blob = new Blob([currentMarkdown], { type: 'text/markdown' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');

    // Sanitize filename
    const safeName = currentSector.replace(/[^a-z0-9]/gi, '_').toLowerCase();

    a.href = url;
    a.download = `market_analysis_${safeName}.md`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

// Allow Enter key to submit
document.getElementById('sectorInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') analyzeMarket();
});
document.getElementById('apiKeyInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') analyzeMarket();
});
