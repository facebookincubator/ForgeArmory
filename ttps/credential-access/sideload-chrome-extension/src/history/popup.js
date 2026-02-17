document.addEventListener('DOMContentLoaded', function() {
  // Calculate the timestamp for the beginning of today
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const startTime = today.getTime();
  
  // Query the history for items from today
  chrome.history.search({
    text: '',          // Return all history items
    startTime: startTime,  // From the beginning of today
    maxResults: 100    // Limit to 100 results
  }, function(historyItems) {
    displayHistory(historyItems);
  });
  
  // Display the history items
  function displayHistory(historyItems) {
    const historyList = document.getElementById('history-list');
    
    if (historyItems.length === 0) {
      historyList.innerHTML = 'No browsing history for today.';
      return;
    }
    
    let historyHTML = '';
    
    historyItems.forEach(function(item) {
      const visitTime = new Date(item.lastVisitTime).toLocaleTimeString();
      
      historyHTML += `
        <div class="history-item">
          <div class="time">${visitTime}</div>
          <div class="title">${item.title || 'No title'}</div>
          <div class="url">${item.url}</div>
        </div>
      `;
    });
    
    historyList.innerHTML = historyHTML;
  }
});
