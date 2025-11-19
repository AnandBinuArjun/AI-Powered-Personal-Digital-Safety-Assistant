// Background script for the Safety Assistant extension

// Create context menu item for scanning links
chrome.runtime.onInstalled.addListener(function() {
  chrome.contextMenus.create({
    id: 'scanLink',
    title: 'Scan link with Safety Assistant',
    contexts: ['link']
  });
});

// Handle context menu clicks
chrome.contextMenus.onClicked.addListener(function(info, tab) {
  if (info.menuItemId === 'scanLink') {
    // Send link to analysis
    analyzeLink(info.linkUrl);
  }
});

// Listen for messages from content scripts
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === 'analyzeUrl') {
    analyzeLink(request.url);
    sendResponse({status: 'analysis started'});
  }
  
  return true; // Keep message channel open for async response
});

function analyzeLink(url) {
  // In a real implementation, you would send this to your backend API
  // For demo purposes, we'll simulate a response and show a notification
  
  console.log('Analyzing URL:', url);
  
  // Simulate API call delay
  setTimeout(() => {
    // Simulate response
    const isSafe = Math.random() > 0.2; // 80% chance of being safe
    
    // Show notification
    chrome.notifications.create({
      type: 'basic',
      iconUrl: 'icons/icon48.png',
      title: 'Safety Assistant',
      message: isSafe 
        ? `This link appears to be safe: ${url}` 
        : `Warning: This link may be unsafe: ${url}`,
      priority: 2
    });
    
    // If unsafe, send message to content script to show warning
    if (!isSafe && sender.tab) {
      chrome.tabs.sendMessage(sender.tab.id, {
        action: 'showWarning',
        message: 'A link on this page has been flagged as potentially unsafe.'
      });
    }
  }, 1000);
}

// Auto-scan URLs as they are visited
chrome.webNavigation.onCompleted.addListener(function(details) {
  // Only scan main frame (not iframes)
  if (details.frameId === 0) {
    // In a real implementation, you might check user settings
    // to see if auto-scan is enabled
    
    // For demo purposes, we'll skip auto-scanning to avoid too many notifications
    console.log('Visited URL:', details.url);
  }
});