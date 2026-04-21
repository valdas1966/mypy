// f_tex_editor Chrome extension — background service worker.
// Extracts a Drive fileId from the active tab URL and opens the
// local editor at http://127.0.0.1:5000/drive-ui/open?fileId=<id>.

const EDITOR_URL = 'http://127.0.0.1:5000/drive-ui/open?fileId=';

// Drive file pages look like:
//   https://drive.google.com/file/d/<FILE_ID>/view
// (optionally with query params / fragments).
function fileIdFromUrl(url) {
  if (!url) return null;
  const m = url.match(/\/file\/d\/([^/?#]+)/);
  return m ? m[1] : null;
}

async function openCurrent(tab) {
  if (!tab) return;
  const id = fileIdFromUrl(tab.url);
  if (!id) {
    // Visible feedback: badge + updated title on the action icon.
    chrome.action.setBadgeText({ text: '!', tabId: tab.id });
    chrome.action.setBadgeBackgroundColor(
      { color: '#a1260d', tabId: tab.id },
    );
    chrome.action.setTitle({
      title:
        'Not a Drive file page. Open a file at ' +
        'drive.google.com/file/d/<id>/view first.',
      tabId: tab.id,
    });
    return;
  }
  await chrome.tabs.create({
    url: EDITOR_URL + encodeURIComponent(id),
    index: tab.index + 1,
  });
}

// Toolbar icon click.
chrome.action.onClicked.addListener(openCurrent);

// Keyboard shortcut (Alt+T by default).
chrome.commands.onCommand.addListener(async (cmd) => {
  if (cmd !== 'open-in-tex-editor') return;
  const [tab] = await chrome.tabs.query({
    active: true,
    currentWindow: true,
  });
  await openCurrent(tab);
});

// Clear stale badge when the user navigates away from Drive.
chrome.tabs.onUpdated.addListener((tabId, info, tab) => {
  if (info.status !== 'complete') return;
  if (fileIdFromUrl(tab.url)) {
    chrome.action.setBadgeText({ text: '', tabId });
    chrome.action.setTitle(
      { title: 'Open in f_tex_editor', tabId },
    );
  }
});
