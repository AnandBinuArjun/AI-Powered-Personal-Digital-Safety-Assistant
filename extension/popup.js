document.addEventListener('DOMContentLoaded', function() {
  const scanButton = document.getElementById('scanButton');
  const statusDiv = document.getElementById('status');
  const feedbackSection = document.getElementById('feedbackSection');
  const feedbackForm = document.getElementById('feedbackForm');
  const falsePositiveBtn = document.getElementById('falsePositiveBtn');
  const falseNegativeBtn = document.getElementById('falseNegativeBtn');
  
  let currentScanId = null;
  
  // Get current safety score from storage
  chrome.storage.local.get(['safetyScore'], function(result) {
    if (result.safetyScore) {
      updateScoreDisplay(result.safetyScore);
    }
  });
  
  scanButton.addEventListener('click', function() {
    statusDiv.textContent = 'Scanning...';
    statusDiv.className = 'status status-loading';
    
    // Get the current tab
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      const currentTab = tabs[0];
      
      // Send message to content script to get page info
      chrome.tabs.sendMessage(currentTab.id, {action: 'getPageInfo'}, function(response) {
        if (chrome.runtime.lastError) {
          statusDiv.textContent = 'Error: ' + chrome.runtime.lastError.message;
          statusDiv.className = 'status status-error';
          return;
        }
        
        // Send to backend for analysis
        analyzeUrl(response.url);
      });
    });
  });
  
  function analyzeUrl(url) {
    // In a real implementation, you would send this to your backend API
    // For demo purposes, we'll simulate a response
    
    setTimeout(() => {
      // Simulate API response
      const isSafe = Math.random() > 0.3; // 70% chance of being safe
      const newScore = isSafe ? Math.floor(Math.random() * 30) + 70 : Math.floor(Math.random() * 40) + 10;
      
      // Save to storage
      chrome.storage.local.set({safetyScore: newScore});
      
      // Update UI
      updateScoreDisplay(newScore);
      
      if (isSafe) {
        statusDiv.textContent = 'Page is safe!';
        statusDiv.className = 'status status-loading';
        feedbackSection.style.display = 'none';
      } else {
        statusDiv.textContent = 'Warning: Potentially unsafe page detected!';
        statusDiv.className = 'status status-error';
        
        // Show warning banner on page
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
          chrome.tabs.sendMessage(tabs[0].id, {
            action: 'showWarning',
            message: 'This page has been flagged as potentially unsafe.'
          });
        });
        
        // Show feedback section
        feedbackSection.style.display = 'block';
        currentScanId = Math.floor(Math.random() * 10000); // Simulate scan ID
      }
    }, 1500);
  }
  
  function updateScoreDisplay(score) {
    const scoreContainer = document.querySelector('.score-container');
    const scoreValue = document.querySelector('.score-value');
    
    scoreValue.textContent = score + '/100';
    
    // Update styling based on score
    scoreContainer.className = 'score-container ' + 
      (score > 70 ? 'score-high' : score > 40 ? 'score-medium' : 'score-low');
  }
  
  // Feedback functionality
  falsePositiveBtn.addEventListener('click', function() {
    submitFeedback(false, "This site was flagged incorrectly");
  });
  
  falseNegativeBtn.addEventListener('click', function() {
    submitFeedback(true, "This site should have been flagged");
  });
  
  feedbackForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const comment = document.getElementById('feedbackComment').value;
    submitFeedback(null, comment);
  });
  
  function submitFeedback(isCorrect, comment) {
    // In a real implementation, you would send feedback to your backend
    console.log('Submitting feedback:', { scanId: currentScanId, isCorrect, comment });
    
    // Show confirmation
    statusDiv.textContent = 'Thank you for your feedback!';
    statusDiv.className = 'status status-loading';
    
    // Hide feedback section
    feedbackSection.style.display = 'none';
    
    // Clear form
    document.getElementById('feedbackComment').value = '';
  }
});