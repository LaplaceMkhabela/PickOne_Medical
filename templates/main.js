const searchFieldEl = document.getElementById('search_field')
const searchBtnEl = document.getElementById('search_btn')

async function fetchPatientData() {
    const outputAreaEl = document.getElementById('output');
    outputAreaEl.textContent = 'Fetching data... please wait.';

    try {
        // Use a free API endpoint for demonstration
        const response = await fetch('https://example.com');

        // Check if the request was successful
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Parse the JSON response body
        const data = await response.json();

        // Display the data in the HTML output area
        outputAreaEl.textContent = `Data fetched successfully! User name: ${data.name || 'N/A'}. Location: ${data.location || 'N/A'}`;
        
    } catch (error) {
        // Handle any errors that occurred during the fetch operation
        console.error('Fetch error:', error);
        outputAreaEl.textContent = `Failed to fetch data: ${error.message}`;
    }
}

// Get the button element and attach an event listener
const fetchButton = document.getElementById('fetchButton');

if (searchBtnEl) {
    // When the button is clicked, execute the fetchUserData function
    searchBtnEl.addEventListener('click', fetchPatientData);
} else {
    console.error('Button not found.');
}
