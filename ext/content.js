// content.js

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log("Received URL:", message.url);

    let pageTitle = document.title;
    console.log("Page title:", pageTitle);

    // remove everything after "Chapter" in the title
    pageTitle = pageTitle.replace(/Chapter\s.*$/, '');

    const match = message.url.match(/(?:chapter[_-])(\d+(?:\.\d+)?)/i);

    if (match && match[1]) {
        const chapterNumber = parseFloat(match[1]);
        console.log("Chapter number:", chapterNumber);

        // append chapter number to the title
        pageTitle += `Chapter ${chapterNumber}`;
    }

    console.log("Modified title:", pageTitle)
    
    // send the URL and title to python script
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
