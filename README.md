# FileDiff

A visual side-by-side file diff and merge GUI. Two flavours, same UX:

| | runtime | install needed | save back to original |
|---|---|---|---|
| `filediff.html` | any modern browser | **none** — double-click the file | yes, in Chromium/Edge/Safari (File System Access API); download fallback elsewhere |
| `filediff`      | Python 3 + Tk      | `python3-tk` on Linux; bundled on macOS/Windows installs | yes |

## Browser version (recommended — OS-independent)

Just open `filediff.html` in any browser:

```
open filediff.html         # macOS
xdg-open filediff.html     # Linux
start filediff.html        # Windows
```

Or drag the file onto a browser window. No build step, no dependencies.

- Click **Open Left** / **Open Right**, or drag-and-drop two files anywhere on the page.
- Click `→` / `←` in the middle gutter to merge each hunk.
- **Save Left** / **Save Right** writes back to the original file (in Chromium/Edge/Safari), or downloads the modified file elsewhere.

## Native version (Python + Tk)

The shebang and exec bit are set, so run it directly:

```
./filediff                          # empty, pick files from File menu
./filediff left.txt right.txt       # open two files directly
```

To install as a system command:

```
ln -s "$PWD/filediff" ~/.local/bin/filediff
filediff left.txt right.txt
```

## Features (both versions)

- Side-by-side panes with color-coded hunks
  - red = deleted (only on left)
  - green = inserted (only on right)
  - yellow = changed on both sides
  - grey = padding to keep panes aligned
- Per-hunk merge arrows in the middle gutter
- Synchronized vertical scrolling
- Save / Save As for each side
- `F8` / `Shift+F8` to jump to next / previous diff

## Requirements

- **Browser version**: any modern browser. Save-back-to-original needs File System Access API (Chrome/Edge 86+, Safari 15.2+). Older browsers fall back to a download.
- **Python version**: Python 3.9+ with Tkinter. On Linux: `sudo apt-get install python3-tk`.
