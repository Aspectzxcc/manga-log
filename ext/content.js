// content.js

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log("Received URL:", message.url);

    const pageTitle = document.title;
    console.log("Page title:", pageTitle);
    
    // Send the URL and title to a Python script
    fetch('http://localhost:8000', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: message.url, title: pageTitle })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(data => {
        console.log('Response:', data.message);
    })
    .catch(error => {
        console.error('Error:', error.message);
    });
});
