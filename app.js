document.addEventListener('DOMContentLoaded', function () {
    fetch('https://raw.githubusercontent.com/turian/llm-arxiv-perplexity/gpu/data/2024-05-01-20%3A45%3A31/final.jsonl')
    .then(response => response.text())
    .then(text => {
        const lines = text.trim().split('\n');
        const minPpl = 1;
        const maxPpl = 32;
        const logMin = Math.log10(minPpl);
        const logMax = Math.log10(maxPpl);

        document.getElementById('ticks1cell').innerHTML = createTicks([1.0, 2.0, 4.0, 8.0, 16, 32], logMin, logMax);
        document.getElementById('ticks2cell').innerHTML = createTicks2([1.0, 2.0, 4.0, 8.0, 16, 32], logMin, logMax);

        lines.forEach(line => {
            const data = JSON.parse(line);
            addRow(data.model, data.ppl, logMin, logMax);
        });
    })
    .catch(err => console.error('Failed to load data:', err));
});

function addRow(model, ppl, logMin, logMax) {
    const tbody = document.getElementById('dataRows');
    const logPpl = Math.log10(ppl);
    const widthPercent = ((logPpl - logMin) / (logMax - logMin)) * 100;

    // Split model[0] at the first occurrence of '_'
    const underscoreIndex = model[0].indexOf('_');
    const firstPart = model[0].substring(0, underscoreIndex);
    const secondPart = model[0].substring(underscoreIndex + 1);
    const model_url = `${firstPart}/${secondPart}`;

    // Data row
    const row = `<tr>
                   <td><a href="https://huggingface.co/${model_url}">${model_url}</a><br>${model[1]}</td>
                   <td>${ppl.toFixed(2)}</td>
                   <td><div class="ppl-bar" style="width: ${widthPercent}%;">${ppl.toFixed(2)}</div></td>
                 </tr>`;

    tbody.innerHTML += row;
}


function createTicks(tickValues, logMin, logMax) {
    return '<div class="tick-marks" style="width: 100%; position: relative;">' + tickValues.map(value => {
        const logValue = Math.log10(value);
        const position = ((logValue - logMin) / (logMax - logMin)) * 100;
        return `<span class="tick" style="left: ${position}%; transform: translateX(-50%);">${value}</span>`;
    }).join('') + '</div>';
}

function createTicks2(tickValues, logMin, logMax) {
    return '<div class="tick-marks" style="width: 100%; position: relative;">' + tickValues.map(value => {
        const logValue = Math.log10(value);
        const position = ((logValue - logMin) / (logMax - logMin)) * 100;
        return `<span class="tick" style="left: ${position}%; transform: translateX(-50%);">|</span>`;
    }).join('') + '</div>';
}
