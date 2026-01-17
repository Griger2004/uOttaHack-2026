# uOttaHack-2026

## Page Title Extractor - Chrome Extension

A simple Chrome extension that reads the current webpage and displays its title in a sleek popup interface.

### Features

- 📄 **Extract Page Title** - Instantly see the title of any webpage
- 🔗 **View URL** - Display the full URL of the current page
- 📋 **Copy to Clipboard** - One-click copy of the page title

### Installation

Follow these steps to install the extension in Chrome:

1. **Download/Clone the repository**
   ```bash
   git clone <repository-url>
   ```

2. **Open Chrome Extensions Page**
   - Open Google Chrome
   - Navigate to `chrome://extensions/` in the address bar
   - Or go to Menu (⋮) → Extensions → Manage Extensions

3. **Enable Developer Mode**
   - Toggle the **Developer mode** switch in the top-right corner of the page

4. **Load the Extension**
   - Click the **Load unpacked** button
   - Browse to and select the `chrome-extension` folder from this project

5. **Pin the Extension (Optional)**
   - Click the puzzle piece icon (🧩) in Chrome's toolbar
   - Click the pin icon next to "Page Title Extractor" to keep it visible

### Usage

1. Navigate to any webpage
2. Click the extension icon in your Chrome toolbar
3. View the page title and URL in the popup
4. Click **Copy Title** to copy the title to your clipboard

### Project Structure

```
chrome-extension/
├── manifest.json    # Extension configuration (Manifest V3)
├── popup.html       # Popup UI structure
├── popup.css        # Styling with dark theme
└── popup.js         # Logic to extract page info
```

### Adding Custom Icons (Optional)

To add custom icons, place PNG files in the `chrome-extension` folder:
- `icon16.png` - 16x16 pixels (toolbar icon)
- `icon48.png` - 48x48 pixels (extensions page)
- `icon128.png` - 128x128 pixels (Chrome Web Store)

### Development

To modify the extension:

1. Make changes to the source files
2. Go to `chrome://extensions/`
3. Click the refresh icon (🔄) on the extension card
4. Test your changes

### License

MIT License - Feel free to use and modify!
