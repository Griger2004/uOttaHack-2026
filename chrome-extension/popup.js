// Get current tab info and extract page title
async function getPageInfo() {
  const titleElement = document.getElementById('page-title');
  const urlElement = document.getElementById('page-url');
  const copyBtn = document.getElementById('copy-btn');

  try {
    // Get the current active tab
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    if (tab) {
      // Display the title
      const title = tab.title || 'No title found';
      titleElement.textContent = title;

      // Display the URL
      const url = tab.url || 'No URL found';
      urlElement.textContent = url;

      // Set up copy button
      copyBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(title).then(() => {
          copyBtn.textContent = 'Copied!';
          copyBtn.classList.add('copied');
          
          setTimeout(() => {
            copyBtn.textContent = 'Copy Title';
            copyBtn.classList.remove('copied');
          }, 2000);
        }).catch(err => {
          console.error('Failed to copy:', err);
          copyBtn.textContent = 'Failed to copy';
        });
      });
    } else {
      titleElement.textContent = 'No active tab found';
      titleElement.classList.add('error');
      urlElement.textContent = '-';
    }
  } catch (error) {
    console.error('Error getting page info:', error);
    titleElement.textContent = 'Error: ' + error.message;
    titleElement.classList.add('error');
    urlElement.textContent = '-';
  }
}

// Run when popup opens
document.addEventListener('DOMContentLoaded', getPageInfo);
