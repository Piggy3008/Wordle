import tkinter as tk
from tkinter import messagebox
import random, os

WORD_LENGTH = 5
MAX_ATTEMPTS = 6

def load_word_list():
    path = os.path.join(os.path.dirname(__file__), "words.txt")
    if os.path.exists(path):
        words = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                w = line.strip().lower()
                if len(w) == WORD_LENGTH and w.isalpha():
                    words.append(w)
        if words:
            return words

WORD_LIST = load_word_list()

class WordleApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wordle")
        self.resizable(False, False)
        self.configure(padx=10, pady=10)

        self.attempt = 0
        self.current_guess = ""
        self.grid_labels = []
        self.secret = random.choice(WORD_LIST)
        self.locked = False

        # Header
        ctrl_frame = tk.Frame(self)
        ctrl_frame.pack(pady=(0,10), fill="x")
        self.info_label = tk.Label(ctrl_frame, text="Guess the 5-letter word!", font=("Helvetica", 12))
        self.info_label.pack(side="left")
        tk.Button(ctrl_frame, text="New Game", command=self.new_game).pack(side="right")

        # Grid
        grid_frame = tk.Frame(self)
        grid_frame.pack()
        for r in range(MAX_ATTEMPTS):
            row = []
            for c in range(WORD_LENGTH):
                lbl = tk.Label(grid_frame, text=" ", width=4, height=2, relief="solid", borderwidth=2,
                               font=("Helvetica", 18), bg="white")
                lbl.grid(row=r, column=c, padx=4, pady=4)
                row.append(lbl)
            self.grid_labels.append(row)

        # On-screen keyboard
        kb_frame = tk.Frame(self)
        kb_frame.pack(pady=(10,0))
        self.key_buttons = {}
        keys = ["QWERTYUIOP","ASDFGHJKL","ZXCVBNM"]
        for row in keys:
            rowf = tk.Frame(kb_frame)
            rowf.pack()
            for ch in row:
                b = tk.Button(rowf, text=ch, width=4, command=lambda ch=ch: self.on_key(ch))
                b.pack(side="left", padx=2, pady=3)
                self.key_buttons[ch] = b

        # Extra control keys
        extra_frame = tk.Frame(kb_frame)
        extra_frame.pack()
        tk.Button(extra_frame, text="Enter", width=6, command=self.submit_guess).pack(side="left", padx=3, pady=3)
        tk.Button(extra_frame, text="Backspace", width=9, command=self.backspace).pack(side="left", padx=3, pady=3)

        # Bind keyboard shortcuts
        self.bind_all("<Key>", self.handle_key)

    def handle_key(self, event):
        if self.locked:
            return
        char = event.keysym.upper()
        if len(char) == 1 and char.isalpha():
            self.on_key(char)
        elif char == "RETURN":
            self.submit_guess()
        elif char == "BACKSPACE":
            self.backspace()

    def on_key(self, ch):
        if self.locked:
            return
        if len(self.current_guess) < WORD_LENGTH:
            self.current_guess += ch.lower()
            self.update_current_row()

    def backspace(self):
        if self.locked:
            return
        if len(self.current_guess) > 0:
            self.current_guess = self.current_guess[:-1]
            self.update_current_row()

    def update_current_row(self):
        row = self.attempt
        for i in range(WORD_LENGTH):
            lbl = self.grid_labels[row][i]
            lbl["text"] = self.current_guess[i].upper() if i < len(self.current_guess) else " "

    def submit_guess(self):
        if self.locked:
            return
        guess = self.current_guess.strip().lower()
        if len(guess) != WORD_LENGTH:
            messagebox.showwarning("Invalid", f"Enter a {WORD_LENGTH}-letter word.")
            return

        # NEW: validate word existence
        if guess not in WORD_LIST:
            messagebox.showwarning("Not in list", "Word not recognized.")
            return

        row = self.attempt
        feedback = ["absent"] * WORD_LENGTH
        secret_chars = list(self.secret)

        # Green pass
        for i in range(WORD_LENGTH):
            if guess[i] == secret_chars[i]:
                feedback[i] = "correct"
                secret_chars[i] = None

        # Yellow pass
        for i in range(WORD_LENGTH):
            if feedback[i] == "correct":
                continue
            if guess[i] in secret_chars:
                feedback[i] = "present"
                secret_chars[secret_chars.index(guess[i])] = None

        # Apply feedback to grid and keyboard
        for i, fb in enumerate(feedback):
            lbl = self.grid_labels[row][i]
            letter = guess[i].upper()
            color = "#787c7e"  # gray
            if fb == "correct":
                color = "#6aaa64"
            elif fb == "present":
                color = "#c9b458"
            lbl["bg"] = color
            lbl["fg"] = "white"

            btn = self.key_buttons.get(letter)
            if btn:
                current = btn.cget("bg")
                new_color = None
                if fb == "correct":
                    new_color = "#6aaa64"
                elif fb == "present":
                    if current not in ("#6aaa64", "#c9b458"):
                        new_color = "#c9b458"
                elif fb == "absent":
                    if current not in ("#6aaa64", "#c9b458", "#787c7e"):
                        new_color = "#787c7e"
                if new_color:
                    btn.config(bg=new_color, fg="white")

        self.attempt += 1
        self.current_guess = ""
        if guess == self.secret:
            messagebox.showinfo("Congratulations!", f"You guessed the word: {self.secret.upper()}!")
            self.locked = True
        elif self.attempt >= MAX_ATTEMPTS:
            messagebox.showinfo("Game Over", f"The word was: {self.secret.upper()}")
            self.locked = True

        self.status_label["text"] = f"Attempt {self.attempt}/{MAX_ATTEMPTS}"

    def new_game(self):
        self.attempt = 0
        self.current_guess = ""
        self.secret = random.choice(WORD_LIST)
        self.locked = False
        for r in range(MAX_ATTEMPTS):
            for c in range(WORD_LENGTH):
                lbl = self.grid_labels[r][c]
                lbl["text"] = " "
                lbl["bg"] = "white"
                lbl["fg"] = "black"
        for btn in self.key_buttons.values():
            btn.config(bg="SystemButtonFace", fg="black")
        self.status_label["text"] = f"Round: 1 | Secret word chosen."
        self.info_label["text"] = "Guess the 5-letter word!"

if __name__ == "__main__":
    app = WordleApp()
    app.mainloop()
