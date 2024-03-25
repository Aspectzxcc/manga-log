// background.js
  
chrome.webNavigation.onCompleted.addListener((details) => {
  if (details.url && details.url.includes("mangakakalot.com/chapter")) {
    console.log("URL matches mangakakalot.com/chapter:", details.url);
    
    chrome.tabs.sendMessage(details.tabId, {
      url: details.url
    });
  }
});
