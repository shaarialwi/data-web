document.addEventListener('DOMContentLoaded', () => {
    // 1. Fetch the data
    fetch('data.json')
        .then(response => response.json())
        .then(data => {
            initializeDashboard(data);
        })
        .catch(error => console.error('Error loading data:', error));
});

function initializeDashboard(data) {
    // Format numbers with commas
    const fmt = (num) => new Intl.NumberFormat('en-US').format(num);

    // 2. Populate top stats
    document.getElementById('total-calon').textContent = data.total_calon;
    document.getElementById('total-pengundi').textContent = fmt(data.total_pengundi);

    // 3. Render the DUN list
    const dunsList = document.getElementById('duns-list');
    
    data.duns.forEach(dun => {
        const div = document.createElement('div');
        div.className = 'dun-item';
        div.innerHTML = `
            <strong>${dun.code} ${dun.name}</strong> 
            <span>${fmt(dun.voters)}</span>
        `;
        
        // Add click event to show details on the right
        div.addEventListener('click', () => displayDunDetails(dun, fmt));
        dunsList.appendChild(div);
    });

    // Optional: Select the first DUN by default
    if (data.duns.length > 0) {
        displayDunDetails(data.duns[0], fmt);
    }
}

function displayDunDetails(dun, fmt) {
    // Update headers
    document.getElementById('dun-code').textContent = dun.code;
    document.getElementById('dun-name').textContent = dun.name;
    document.getElementById('dun-voters').textContent = `${fmt(dun.voters)} JUMLAH PENGUNDI BERDAFTAR`;

    // Render Candidates
    const candidatesList = document.getElementById('candidates-list');
    candidatesList.innerHTML = ''; // Clear previous

    if (dun.cands && dun.cands.length > 0) {
        dun.cands.forEach(cand => {
            const candDiv = document.createElement('div');
            candDiv.className = 'candidate-card';
            candDiv.innerHTML = `<strong>${cand.name}</strong> <br> <small>${cand.party}</small>`;
            candidatesList.appendChild(candDiv);
        });
    } else {
        candidatesList.innerHTML = '<p>Tiada data calon.</p>';
    }

    // Render Incumbent
    const incumbentName = document.getElementById('incumbent-name');
    if (dun.inc && dun.inc.length === 2) {
        incumbentName.textContent = `${dun.inc[0]} (${dun.inc[1]})`;
    } else {
        incumbentName.textContent = 'Tiada Maklumat';
    }
}
