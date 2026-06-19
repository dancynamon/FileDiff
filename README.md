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

- **Open Left ▾** / **Open Right ▾** → pick **File…** or **Folder…**.
- Or drag-and-drop one/two files **or** two folders anywhere on the page.
- In folder mode, the file list at the top shows every path with a status icon
  (`=` identical, `≠` differs, `←` only-left, `→` only-right). Click a row to
  open that file pair in the diff view.
- Click `→` / `←` in the middle gutter to merge each hunk.
- **Save Left** / **Save Right** writes back to the original file (in Chromium/Edge),
  including writing new files into a folder when one side was missing.

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

## Features

- Side-by-side panes with color-coded hunks
  - red = deleted (only on left)
  - green = inserted (only on right)
  - yellow = changed on both sides
  - grey = padding to keep panes aligned
- Per-hunk merge arrows in the middle gutter
- Synchronized vertical scrolling
- Save / Save As for each side
- `F8` / `Shift+F8` to jump to next / previous diff
- **Folder diff (browser version)**: open two folders, walk recursively,
  per-file status, click-through to file diffs, save back to disk

## Requirements

- **Browser version**: any modern browser. Save-back-to-original needs File System Access API (Chrome/Edge 86+, Safari 15.2+). Older browsers fall back to a download.
- **Python version**: Python 3.9+ with Tkinter. On Linux: `sudo apt-get install python3-tk`.
