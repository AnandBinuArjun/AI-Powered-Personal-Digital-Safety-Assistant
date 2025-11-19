// Content script that runs on web pages

// Listen for messages from popup or background script
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === 'getPageInfo') {
    // Send back page information
    sendResponse({
      url: window.location.href,
      title: document.title
    });
  } else if (request.action === 'showWarning') {
    // Show warning banner on page
    showWarningBanner(request.message);
    sendResponse({status: 'banner shown'});
  }
  
  return true; // Keep message channel open for async response
});

function showWarningBanner(message) {
  // Check if banner already exists
  if (document.getElementById('safety-assistant-banner')) {
    return;
  }
  
  // Create warning banner
  const banner = document.createElement('div');
  banner.id = 'safety-assistant-banner';
  banner.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background-color: #f44336;
    color: white;
    padding: 15px;
    text-align: center;
    z-index: 10000;
    font-family: Arial, sans-serif;
    font-size: 16px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
  `;
  
  banner.innerHTML = `
    <strong>SAFETY WARNING:</strong> ${message}
    <button id="close-banner" style="
      float: right;
      background: none;
      border: none;
      color: white;
      font-size: 20px;
      cursor: pointer;
      margin-left: 10px;
    ">&times;</button>
  `;
  
  // Add close functionality
  banner.addEventListener('click', function(e) {
    if (e.target.id === 'close-banner') {
      banner.remove();
    }
  });
  
  // Insert banner at top of page
  document.body.insertBefore(banner, document.body.firstChild);
  
  // Auto-hide after 10 seconds
  setTimeout(() => {
    if (banner.parentNode) {
      banner.remove();
    }
  }, 10000);
}

// Auto-scan page on load
window.addEventListener('load', function() {
  // In a real implementation, you would check if auto-scan is enabled
  // and then send the current URL to your backend for analysis
  console.log('Safety Assistant: Page loaded - ready for scanning');
});