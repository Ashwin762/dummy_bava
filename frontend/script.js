const API_BASE_URL = 'http://localhost:8000';

// Mock Data
const mockJobs = [
    { company: 'Google', role: 'Software Engineering Intern', location: 'Mountain View, CA', experience: 'Internship', type: 'Full-time', status: 'Not Applied', link: '#' },
    { company: 'NVIDIA', role: 'Deep Learning Intern', location: 'Remote', experience: 'Internship', type: 'Contract', status: 'Saved', link: '#' },
    { company: 'Microsoft', role: 'Software Engineer', location: 'Redmond, WA', experience: 'Fresher', type: 'Full-time', status: 'Applied', link: '#' },
    { company: 'Amazon', role: 'Cloud Support Associate', location: 'Seattle, WA', experience: '0-6 Months', type: 'Full-time', status: 'Not Applied', link: '#' }
];

// DOM Elements
const searchBtn = document.getElementById('searchBtn');
const resetBtn = document.getElementById('resetBtn');
const logsContainer = document.getElementById('logsContainer');
const jobsTableBody = document.getElementById('jobsTableBody');

// State counters
const counters = {
    total: document.getElementById('totalJobsCount'),
    applied: document.getElementById('appliedCount'),
    interview: document.getElementById('interviewCount'),
    saved: document.getElementById('savedCount')
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    renderJobs(mockJobs);
    addLog('System ready. Dashboard loaded successfully.', 'system');
});

// Utility: Add Log
function addLog(message, type = '') {
    const entry = document.createElement('div');
    entry.className = `log-entry ${type}`;
    entry.textContent = `> [${new Date().toLocaleTimeString()}] ${message}`;
    logsContainer.appendChild(entry);
    logsContainer.scrollTop = logsContainer.scrollHeight;
}

// Render Table
function renderJobs(jobs) {
    jobsTableBody.innerHTML = '';
    jobs.forEach(job => {
        const row = document.createElement('tr');
        const statusClass = job.status === 'Applied' ? 'badge-applied' : (job.status === 'Saved' ? 'badge-saved' : '');
        
        row.innerHTML = `
            <td><strong>${job.company}</strong></td>
            <td>${job.role}</td>
            <td>${job.location}</td>
            <td>${job.experience}</td>
            <td>${job.type}</td>
            <td><span class="badge ${statusClass}">${job.status}</span></td>
            <td><a href="${job.link}" class="apply-link" target="_blank">View Role</a></td>
        `;
        jobsTableBody.appendChild(row);
    });
    updateStats(jobs);
}

function updateStats(jobs) {
    counters.total.textContent = jobs.length;
    counters.applied.textContent = jobs.filter(j => j.status === 'Applied').length;
    counters.saved.textContent = jobs.filter(j => j.status === 'Saved').length;
    counters.interview.textContent = 0; // Placeholder
}

// Event Listeners
searchBtn.addEventListener('click', async () => {
    const payload = {
        location: document.getElementById('locationInput').value,
        experience: document.getElementById('experienceInput').value,
        role: document.getElementById('roleInput').value,
        companies: document.getElementById('companyInput').value
    };

    addLog(`Initiating search for "${payload.role}" in "${payload.location}"...`, 'system');
    
    // Simulate Loading
    searchBtn.disabled = true;
    searchBtn.textContent = 'Searching...';

    try {
        /* Uncomment this for real backend integration
        const response = await fetch(`${API_BASE_URL}/api/search`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await response.json();
        renderJobs(data);
        */
        
        // Simulating delay for mock
        setTimeout(() => {
            addLog(`Scraping job portals for ${payload.companies || 'relevant companies'}...`);
            addLog(`Found ${mockJobs.length} matches.`);
            renderJobs(mockJobs);
            searchBtn.disabled = false;
            searchBtn.textContent = 'Search Opportunities';
        }, 1500);

    } catch (error) {
        addLog(`Error: ${error.message}`, 'system');
        searchBtn.disabled = false;
    }
});

resetBtn.addEventListener('click', () => {
    document.querySelectorAll('input').forEach(i => i.value = '');
    addLog('Filters cleared.');
    renderJobs(mockJobs);
});

async function exportData(format) {
    addLog(`Generating ${format.toUpperCase()} export...`);
    // Placeholder for window.location.href = `${API_BASE_URL}/api/export/${format}`;
    setTimeout(() => addLog(`Success: OpportunityOS_${format}_report.zip downloaded.`, 'system'), 1000);
}

document.getElementById('exportExcelBtn').onclick = () => exportData('excel');
document.getElementById('exportCsvBtn').onclick = () => exportData('csv');