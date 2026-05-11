#!/usr/bin/env python3
"""FileDiff -- a visual side-by-side file diff and merge GUI.

Usage:
    python3 filediff.py [left_file right_file]

Pure Tkinter / stdlib. No external dependencies.
"""

from __future__ import annotations

import difflib
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox


COLOR_DELETE = "#ffd6d6"
COLOR_INSERT = "#d6ffd6"
COLOR_REPLACE = "#ffe9b0"
COLOR_PAD = "#ececec"
COLOR_PAD_FG = "#bbbbbb"
COLOR_HUNK_BG = "#fff5b8"
COLOR_HUNK_BORDER = "#c9b85c"
COLOR_ARROW_R = "#0a66c2"
COLOR_ARROW_L = "#c2660a"

FONT = ("Menlo", 11)


class FileDiffApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("FileDiff")
        self.root.geometry("1400x800")

        self.left_path: Path | None = None
        self.right_path: Path | None = None
        self.left_lines: list[str] = []
        self.right_lines: list[str] = []
        self.left_trailing_nl = True
        self.right_trailing_nl = True
        self.hunks: list[dict] = []
        self._syncing = False

        self._build_menu()
        self._build_ui()

    # ---------- UI construction ----------

    def _build_menu(self) -> None:
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        filemenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Open Left...",
                             accelerator="Ctrl+L",
                             command=self.open_left)
        filemenu.add_command(label="Open Right...",
                             accelerator="Ctrl+R",
                             command=self.open_right)
        filemenu.add_separator()
        filemenu.add_command(label="Save Left",
                             accelerator="Ctrl+S",
                             command=self.save_left)
        filemenu.add_command(label="Save Right",
                             accelerator="Ctrl+Shift+S",
                             command=self.save_right)
        filemenu.add_command(label="Save Left As...",
                             command=lambda: self.save_left(as_new=True))
        filemenu.add_command(label="Save Right As...",
                             command=lambda: self.save_right(as_new=True))
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=self.root.quit)

        editmenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Navigate", menu=editmenu)
        editmenu.add_command(label="Next Diff", accelerator="F8",
                             command=self.next_diff)
        editmenu.add_command(label="Previous Diff", accelerator="Shift+F8",
                             command=self.prev_diff)

        self.root.bind_all("<Control-l>", lambda e: self.open_left())
        self.root.bind_all("<Control-r>", lambda e: self.open_right())
        self.root.bind_all("<Control-s>", lambda e: self.save_left())
        self.root.bind_all("<Control-S>", lambda e: self.save_right())
        self.root.bind_all("<F8>", lambda e: self.next_diff())
        self.root.bind_all("<Shift-F8>", lambda e: self.prev_diff())

    def _build_ui(self) -> None:
        toolbar = tk.Frame(self.root, bg="#e6e6e6")
        toolbar.pack(side="top", fill="x")

        def tb_button(text, cmd):
            return tk.Button(toolbar, text=text, command=cmd,
                             relief="flat", bg="#e6e6e6",
                             activebackground="#d0d0d0",
                             padx=8, pady=4)

        tb_button("Open Left", self.open_left).pack(side="left", padx=2, pady=2)
        tb_button("Open Right", self.open_right).pack(side="left", padx=2, pady=2)
        tb_button("Refresh", self.recompute_diff).pack(side="left", padx=2, pady=2)
        tk.Frame(toolbar, width=20, bg="#e6e6e6").pack(side="left")
        tb_button("← Prev", self.prev_diff).pack(side="left", padx=2, pady=2)
        tb_button("Next →", self.next_diff).pack(side="left", padx=2, pady=2)

        tb_button("Save Right", self.save_right).pack(side="right", padx=2, pady=2)
        tb_button("Save Left", self.save_left).pack(side="right", padx=2, pady=2)

        # Path labels
        labels = tk.Frame(self.root, bg="#d6d6d6")
        labels.pack(side="top", fill="x")
        self.left_label = tk.Label(labels, text="(no file)", anchor="w",
                                   bg="#d6d6d6", padx=6)
        self.left_label.grid(row=0, column=0, sticky="ew")
        tk.Label(labels, text="", bg="#d6d6d6", width=8).grid(row=0, column=1)
        self.right_label = tk.Label(labels, text="(no file)", anchor="w",
                                    bg="#d6d6d6", padx=6)
        self.right_label.grid(row=0, column=2, sticky="ew")
        labels.columnconfigure(0, weight=1)
        labels.columnconfigure(2, weight=1)

        # Main split
        main = tk.Frame(self.root)
        main.pack(side="top", fill="both", expand=True)
        main.columnconfigure(0, weight=1)
        main.columnconfigure(2, weight=1)
        main.rowconfigure(0, weight=1)

        self.left_text = self._make_text(main)
        self.left_text.grid(row=0, column=0, sticky="nsew")

        self.middle = tk.Canvas(main, width=64, bg="#f4f4f4",
                                highlightthickness=0)
        self.middle.grid(row=0, column=1, sticky="ns")

        self.right_text = self._make_text(main)
        self.right_text.grid(row=0, column=2, sticky="nsew")

        self.vsb = tk.Scrollbar(main, orient="vertical", command=self._on_vsb)
        self.vsb.grid(row=0, column=3, sticky="ns")
        self.left_text.config(yscrollcommand=self._on_yscroll)
        self.right_text.config(yscrollcommand=self._on_yscroll)

        # Horizontal scrollbars
        self.left_hsb = tk.Scrollbar(main, orient="horizontal",
                                     command=self.left_text.xview)
        self.left_hsb.grid(row=1, column=0, sticky="ew")
        self.left_text.config(xscrollcommand=self.left_hsb.set)
        self.right_hsb = tk.Scrollbar(main, orient="horizontal",
                                      command=self.right_text.xview)
        self.right_hsb.grid(row=1, column=2, sticky="ew")
        self.right_text.config(xscrollcommand=self.right_hsb.set)

        # Status bar
        self.status = tk.Label(self.root, text="Open two files to begin.",
                               anchor="w", bg="#eeeeee", padx=6)
        self.status.pack(side="bottom", fill="x")

        # Tags
        for w in (self.left_text, self.right_text):
            w.tag_configure("delete", background=COLOR_DELETE)
            w.tag_configure("insert", background=COLOR_INSERT)
            w.tag_configure("replace", background=COLOR_REPLACE)
            w.tag_configure("pad", background=COLOR_PAD,
                            foreground=COLOR_PAD_FG)

        # Wheel binding
        for w in (self.left_text, self.right_text, self.middle):
            w.bind("<MouseWheel>", self._on_mousewheel)
            w.bind("<Button-4>", self._on_mousewheel)
            w.bind("<Button-5>", self._on_mousewheel)

        # Redraw arrows after resize
        self.root.bind("<Configure>",
                       lambda e: self.middle.after_idle(self._redraw_middle))

    def _make_text(self, parent: tk.Widget) -> tk.Text:
        return tk.Text(parent, wrap="none", font=FONT,
                       undo=False, padx=4, pady=2,
                       state="disabled", cursor="arrow",
                       background="#ffffff")

    # ---------- File I/O ----------

    def open_left(self) -> None:
        path = filedialog.askopenfilename(title="Open Left File")
        if not path:
            return
        self._load_left(path)

    def open_right(self) -> None:
        path = filedialog.askopenfilename(title="Open Right File")
        if not path:
            return
        self._load_right(path)

    def _load_left(self, path: str) -> None:
        lines, trailing = self._read_file(path)
        self.left_path = Path(path)
        self.left_lines = lines
        self.left_trailing_nl = trailing
        self.left_label.config(text=str(path))
        self.recompute_diff()

    def _load_right(self, path: str) -> None:
        lines, trailing = self._read_file(path)
        self.right_path = Path(path)
        self.right_lines = lines
        self.right_trailing_nl = trailing
        self.right_label.config(text=str(path))
        self.recompute_diff()

    def _read_file(self, path: str) -> tuple[list[str], bool]:
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except OSError as e:
            messagebox.showerror("Open failed", f"Could not read {path}:\n{e}")
            return [], True
        trailing = content.endswith("\n") or content == ""
        return content.splitlines(), trailing

    def save_left(self, as_new: bool = False) -> None:
        path = None if as_new else self.left_path
        if path is None:
            chosen = filedialog.asksaveasfilename(title="Save Left As")
            if not chosen:
                return
            path = Path(chosen)
            self.left_path = path
            self.left_label.config(text=str(path))
        self._write_file(path, self.left_lines, self.left_trailing_nl)
        self.status.config(text=f"Saved left -> {path}")

    def save_right(self, as_new: bool = False) -> None:
        path = None if as_new else self.right_path
        if path is None:
            chosen = filedialog.asksaveasfilename(title="Save Right As")
            if not chosen:
                return
            path = Path(chosen)
            self.right_path = path
            self.right_label.config(text=str(path))
        self._write_file(path, self.right_lines, self.right_trailing_nl)
        self.status.config(text=f"Saved right -> {path}")

    def _write_file(self, path: Path, lines: list[str], trailing: bool) -> None:
        content = "\n".join(lines)
        if trailing and (content or not lines == []):
            content += "\n"
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
        except OSError as e:
            messagebox.showerror("Save failed", f"Could not write {path}:\n{e}")

    # ---------- Diff rendering ----------

    def recompute_diff(self) -> None:
        # preserve scroll position
        try:
            top = self.left_text.yview()[0]
        except tk.TclError:
            top = 0.0

        sm = difflib.SequenceMatcher(a=self.left_lines, b=self.right_lines,
                                     autojunk=False)
        opcodes = sm.get_opcodes()

        self.left_text.config(state="normal")
        self.right_text.config(state="normal")
        self.left_text.delete("1.0", "end")
        self.right_text.delete("1.0", "end")

        self.hunks = []
        display_line = 1

        for tag, i1, i2, j1, j2 in opcodes:
            left_chunk = self.left_lines[i1:i2]
            right_chunk = self.right_lines[j1:j2]
            n = max(len(left_chunk), len(right_chunk))
            if n == 0:
                continue

            display_start = display_line

            for k in range(n):
                if k < len(left_chunk):
                    self.left_text.insert("end", left_chunk[k] + "\n")
                else:
                    self.left_text.insert("end", "\n")
                if k < len(right_chunk):
                    self.right_text.insert("end", right_chunk[k] + "\n")
                else:
                    self.right_text.insert("end", "\n")
                display_line += 1

            display_end = display_line  # exclusive

            if tag != "equal":
                left_end_real = display_start + len(left_chunk)
                right_end_real = display_start + len(right_chunk)

                if tag == "delete":
                    self.left_text.tag_add("delete",
                                           f"{display_start}.0",
                                           f"{left_end_real}.0")
                    self.right_text.tag_add("pad",
                                            f"{display_start}.0",
                                            f"{display_end}.0")
                elif tag == "insert":
                    self.right_text.tag_add("insert",
                                            f"{display_start}.0",
                                            f"{right_end_real}.0")
                    self.left_text.tag_add("pad",
                                           f"{display_start}.0",
                                           f"{display_end}.0")
                else:  # replace
                    self.left_text.tag_add("replace",
                                           f"{display_start}.0",
                                           f"{left_end_real}.0")
                    self.right_text.tag_add("replace",
                                            f"{display_start}.0",
                                            f"{right_end_real}.0")
                    if left_end_real < display_end:
                        self.left_text.tag_add("pad",
                                               f"{left_end_real}.0",
                                               f"{display_end}.0")
                    if right_end_real < display_end:
                        self.right_text.tag_add("pad",
                                                f"{right_end_real}.0",
                                                f"{display_end}.0")

                self.hunks.append({
                    "tag": tag,
                    "i1": i1, "i2": i2,
                    "j1": j1, "j2": j2,
                    "display_start": display_start,
                    "display_end": display_end,
                })

        self.left_text.config(state="disabled")
        self.right_text.config(state="disabled")

        # restore scroll
        self.left_text.yview_moveto(top)
        self.right_text.yview_moveto(top)

        n_hunks = len(self.hunks)
        if not self.left_lines and not self.right_lines:
            self.status.config(text="Open two files to begin.")
        elif n_hunks == 0:
            self.status.config(text="Files are identical.")
        else:
            self.status.config(
                text=f"{n_hunks} difference"
                     f"{'s' if n_hunks != 1 else ''}. "
                     "Click → to push left into right, "
                     "← to push right into left."
            )

        self.middle.after_idle(self._redraw_middle)

    # ---------- Middle gutter (merge arrows) ----------

    def _redraw_middle(self) -> None:
        self.middle.delete("all")
        if not self.hunks:
            return

        width = int(self.middle.winfo_width()) or 64

        for idx, hunk in enumerate(self.hunks):
            info_start = self.left_text.dlineinfo(f"{hunk['display_start']}.0")
            info_last = self.left_text.dlineinfo(
                f"{hunk['display_end'] - 1}.0")
            if not info_start or not info_last:
                continue
            y_top = info_start[1]
            y_bot = info_last[1] + info_last[3]
            y_mid = (y_top + y_bot) / 2

            self.middle.create_rectangle(
                2, y_top, width - 2, y_bot,
                fill=COLOR_HUNK_BG, outline=COLOR_HUNK_BORDER, width=1,
            )
            r_tag = f"arr_r_{idx}"
            l_tag = f"arr_l_{idx}"
            self.middle.create_text(
                width * 0.30, y_mid, text="→",
                font=("Menlo", 16, "bold"),
                fill=COLOR_ARROW_R, tags=(r_tag,),
            )
            self.middle.create_text(
                width * 0.70, y_mid, text="←",
                font=("Menlo", 16, "bold"),
                fill=COLOR_ARROW_L, tags=(l_tag,),
            )
            self.middle.tag_bind(
                r_tag, "<Button-1>",
                lambda e, i=idx: self.merge_to_right(i),
            )
            self.middle.tag_bind(
                l_tag, "<Button-1>",
                lambda e, i=idx: self.merge_to_left(i),
            )
            for tag in (r_tag, l_tag):
                self.middle.tag_bind(
                    tag, "<Enter>",
                    lambda e: self.middle.config(cursor="hand2"),
                )
                self.middle.tag_bind(
                    tag, "<Leave>",
                    lambda e: self.middle.config(cursor=""),
                )

    # ---------- Merge operations ----------

    def merge_to_right(self, idx: int) -> None:
        """Copy the left side of hunk `idx` into the right file."""
        if idx >= len(self.hunks):
            return
        h = self.hunks[idx]
        replacement = self.left_lines[h["i1"]:h["i2"]]
        self.right_lines = (self.right_lines[:h["j1"]]
                            + replacement
                            + self.right_lines[h["j2"]:])
        self.recompute_diff()

    def merge_to_left(self, idx: int) -> None:
        """Copy the right side of hunk `idx` into the left file."""
        if idx >= len(self.hunks):
            return
        h = self.hunks[idx]
        replacement = self.right_lines[h["j1"]:h["j2"]]
        self.left_lines = (self.left_lines[:h["i1"]]
                           + replacement
                           + self.left_lines[h["i2"]:])
        self.recompute_diff()

    # ---------- Scroll sync ----------

    def _on_yscroll(self, *args) -> None:
        self.vsb.set(*args)
        if self._syncing:
            return
        self._syncing = True
        try:
            top = float(args[0])
            self.left_text.yview_moveto(top)
            self.right_text.yview_moveto(top)
        finally:
            self._syncing = False
        self.middle.after_idle(self._redraw_middle)

    def _on_vsb(self, *args) -> None:
        self.left_text.yview(*args)
        self.right_text.yview(*args)
        self.middle.after_idle(self._redraw_middle)

    def _on_mousewheel(self, event) -> str:
        if event.num == 4:
            delta = -3
        elif event.num == 5:
            delta = 3
        elif getattr(event, "delta", 0):
            delta = -int(event.delta / 40) or (-1 if event.delta > 0 else 1)
        else:
            delta = 0
        if delta:
            self.left_text.yview_scroll(delta, "units")
        return "break"

    # ---------- Navigation ----------

    def next_diff(self) -> None:
        if not self.hunks:
            return
        try:
            top = self.left_text.yview()[0]
        except tk.TclError:
            return
        total_lines = max(int(self.left_text.index("end-1c").split(".")[0]), 1)
        current_line = top * total_lines + 1
        for h in self.hunks:
            if h["display_start"] > current_line + 0.5:
                target = h["display_start"]
                break
        else:
            target = self.hunks[0]["display_start"]
        self._scroll_to_line(target)

    def prev_diff(self) -> None:
        if not self.hunks:
            return
        try:
            top = self.left_text.yview()[0]
        except tk.TclError:
            return
        total_lines = max(int(self.left_text.index("end-1c").split(".")[0]), 1)
        current_line = top * total_lines + 1
        prev = None
        for h in self.hunks:
            if h["display_start"] < current_line - 0.5:
                prev = h
            else:
                break
        if prev is None:
            prev = self.hunks[-1]
        self._scroll_to_line(prev["display_start"])

    def _scroll_to_line(self, line: int) -> None:
        total_lines = max(int(self.left_text.index("end-1c").split(".")[0]), 1)
        frac = max(0.0, (line - 2) / total_lines)
        self.left_text.yview_moveto(frac)
        self.right_text.yview_moveto(frac)
        self.middle.after_idle(self._redraw_middle)


def main() -> None:
    root = tk.Tk()
    app = FileDiffApp(root)
    if len(sys.argv) >= 3:
        app._load_left(sys.argv[1])
        app._load_right(sys.argv[2])
    root.mainloop()


if __name__ == "__main__":
    main()
