# FileDiff

A visual side-by-side file diff and merge GUI. Pure Python / Tkinter — no
external dependencies.

## Run

The shebang and exec bit are set, so just run it directly:

```
./filediff                          # open empty, pick files from File menu
./filediff left.txt right.txt       # open two files directly
```

To install as a system command, drop it on your `PATH`:

```
ln -s "$PWD/filediff" ~/.local/bin/filediff
filediff left.txt right.txt
```

Or invoke via the interpreter explicitly:

```
python3 filediff left.txt right.txt
```

## Features

- Side-by-side panes with color-coded hunks
  - red = deleted (only on left)
  - green = inserted (only on right)
  - yellow = changed on both sides
  - grey = padding to keep panes aligned
- Per-hunk merge arrows in the middle gutter
  - `→` push the left hunk into the right file
  - `←` push the right hunk into the left file
- Synchronized vertical scrolling and mouse-wheel
- Save / Save As for each side
- `F8` / `Shift+F8` to jump to next / previous diff

## Requirements

Python 3.9+ with Tkinter. On most Linux distros:

```
sudo apt-get install python3-tk
```
