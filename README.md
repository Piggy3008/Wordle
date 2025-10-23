# Wordle Unlimited (Tkinter)

This is a desktop Wordle (Unlimited) implementation using Python and Tkinter.

## Features
- 5-letter Wordle game, 6 attempts per round.
- GUI using Tkinter (grid + on-screen keyboard).
- New Game button for unlimited rounds.
- Built-in small dictionary; you can optionally provide `words.txt` in the same folder
  with one 5-letter word per line to use a larger dictionary.

## Files
- `main.py` — the game source (run with `python main.py`)
- `words.txt` — optional word list (not included)
- `Report.pdf` — short project report (generated)
- `requirements.txt` — optional Python dependencies

## How to run
1. Ensure Python 3 is installed.
2. (Optional) Install dependencies: `pip install -r requirements.txt`
3. Run: `python main.py`

## Notes on submission
The original assignment requested that resource files (dictionaries, icons, etc.) are **not** included in the submission zip. If you want to use a larger dictionary, upload `words.txt` to a cloud drive and include download instructions in `README.md`. This implementation uses a small embedded word list by default to keep the submission lightweight.
