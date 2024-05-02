document.addEventListener('DOMContentLoaded', function () {
    fetch('https://raw.githubusercontent.com/turian/llm-arxiv-perplexity/gpu/data/2024-05-01-20%3A45%3A31/final.jsonl')
    .then(response => response.text())
    .then(text => {
        const lines = text.trim().split('\n');
        lines.forEach(line => {
            const data = JSON.parse(line);
            addRow(data.model, data.ppl);
        });
    })
    .catch(err => console.error('Failed to load data:', err));
});

function addRow(model, ppl) {
    const tbody = document.getElementById('dataRows');
    //const minPpl = 0.1;
    const minPpl = 1;
    const maxPpl = 32;
    // Logarithmic transformation
    const logMin = Math.log10(minPpl);
    const logMax = Math.log10(maxPpl);
    const logPpl = Math.log10(ppl);
    const widthPercent = ((logPpl - logMin) / (logMax - logMin)) * 100;

    // Data row
    let row = `<tr>
                   <td>${model[0]}<br>${model[1]}</td>
                   <td>${ppl.toFixed(2)}</td>
                   <td><div class="ppl-bar" style="width: ${widthPercent}%;">${ppl.toFixed(2)}</div></td>
               </tr>`;

    // Tick row with specified ticks
    row += `<tr class="tick-row">
                <td colspan="2"></td>
                <td>
                    <div class="tick-marks" style="width: 100%; position: relative;">
                        ${createTicks([1.0, 2.0, 4.0, 8.0, 16, 32], logMin, logMax)}
                    </div>
                </td>
            </tr>`;
    // Tick row with specified ticks
    row += `<tr class="tick-row">
                <td colspan="2"></td>
                <td>
                    <div class="tick-marks" style="width: 100%; position: relative;">
                        ${createTicks2([1.0, 2.0, 4.0, 8.0, 16, 32], logMin, logMax)}
                    </div>
                </td>
            </tr>`;

    tbody.innerHTML += row;
}

function createTicks(tickValues, logMin, logMax) {
    return tickValues.map(value => {
        const logValue = Math.log10(value);
        const position = ((logValue - logMin) / (logMax - logMin)) * 100;
        // Using transform to shift the tick so that it ends at the calculated position
        return `<span class="tick" style="left: ${position}%; transform: translateX(-50%);">${value}</span>`;
    }).join('');
}

function createTicks2(tickValues, logMin, logMax) {
    return tickValues.map(value => {
        const logValue = Math.log10(value);
        const position = ((logValue - logMin) / (logMax - logMin)) * 100;
        // Using transform to shift the tick so that it ends at the calculated position
        return `<span class="tick" style="left: ${position}%; transform: translateX(-50%);">|</span>`;
    }).join('');
}