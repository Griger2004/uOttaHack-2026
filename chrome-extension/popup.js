const BACKEND_URL = 'http://localhost:8000';

// Extract article text and send to backend for verification
async function verifyArticle() {
  const summaryElement = document.getElementById('page-summary');

  try {
    summaryElement.textContent = 'Extracting article...';

    // Get the current active tab
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    if (!tab) {
      summaryElement.textContent = 'No active tab found';
      summaryElement.classList.add('error');
      return;
    }

    // Inject script to extract article text
    const results = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: extractArticleText
    });

    if (!results || !results[0] || !results[0].result) {
      summaryElement.textContent = 'Could not extract article text';
      summaryElement.classList.add('error');
      return;
    }

    const articleText = results[0].result;
    
    if (articleText.length < 50) {
      summaryElement.textContent = 'Article text too short to verify';
      summaryElement.classList.add('error');
      return;
    }

    summaryElement.textContent = 'Verifying article...';

    // Send to backend
    const response = await fetch(`${BACKEND_URL}/verify`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ article_text: articleText })
    });

    if (!response.ok) {
      throw new Error(`Backend error: ${response.status}`);
    }

    const result = await response.json();
    
    // Display result
    displayResult(result, summaryElement);

  } catch (error) {
    console.error('Error:', error);
    summaryElement.textContent = 'Error: ' + error.message;
    summaryElement.classList.add('error');
  }
}

// Function to be injected into the page to extract article text
function extractArticleText() {
  // Try to find article content in order of priority
  const selectors = [
    'article',
    '[role="article"]',
    'main',
    '[role="main"]',
    '.article-content',
    '.post-content',
    '.entry-content',
    '.content'
  ];

  let contentElement = null;
  for (const selector of selectors) {
    contentElement = document.querySelector(selector);
    if (contentElement) break;
  }

  // Fallback to body
  if (!contentElement) {
    contentElement = document.body;
  }

  // Clone and clean
  const clone = contentElement.cloneNode(true);
  
  // Remove non-content elements
  const removeSelectors = 'script, style, nav, footer, header, aside, .nav, .menu, .sidebar, .comments, .advertisement, .ad, iframe, form';
  clone.querySelectorAll(removeSelectors).forEach(el => el.remove());

  // Get text content
  let text = clone.innerText || clone.textContent || '';
  
  // Clean up whitespace
  text = text.replace(/\s+/g, ' ').trim();

  return text;
}

// Display the verification result
function displayResult(result, element) {
  const verdictColors = {
    'True': '#00ff88',
    'Fake': '#ff6b6b',
    'Unverified': '#ffaa00'
  };

  const color = verdictColors[result.verdict] || '#ffffff';
  
  element.innerHTML = `
    <div style="margin-bottom: 10px;">
      <strong style="color: ${color}; font-size: 1.2em;">${result.verdict}</strong>
      <span style="color: #888; margin-left: 10px;">Score: ${result.trust_score}/100</span>
    </div>
    <div style="color: #ccc; font-size: 0.9em;">${result.reasoning}</div>
  `;
}

// Run when popup opens
document.addEventListener('DOMContentLoaded', verifyArticle);
