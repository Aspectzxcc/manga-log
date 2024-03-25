// background.js
  
const validURLs = [
  "mangakakalot.com/chapter",
  "chapmanganato.to/"
];

function isValidURL(url) {
  return validURLs.some(validURL => url.includes(validURL));
}

chrome.webNavigation.onCompleted.addListener((details) => {
  if (details.url && isValidURL(details.url)) {
    console.log("URL matches valid pattern:", details.url);

    chrome.tabs.sendMessage(details.tabId, {
      url: details.url
    });
  }
});