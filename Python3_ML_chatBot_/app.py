import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
from data_reader import TravelDataReader
from engine import SimilarityEngine
from tagger import Tagger

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TravelBot Intelligence")
        self.root.geometry("450x700")
        
        # WhatsApp Theme Palette
        self.BG_COLOR = "#E5DDD5"
        self.HEADER_COLOR = "#075E54"
        self.USER_BUBBLE = "#DCF8C6"
        self.BOT_BUBBLE = "#FFFFFF"

        self.initialize_backend()
        self.setup_ui()
        self.tagger = Tagger()

    def initialize_backend(self):
        reader = TravelDataReader('travel_data.csv')
        if reader.load():
            self.engine = SimilarityEngine(reader.questions, reader.answers)
        else:
            self.engine = None

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.HEADER_COLOR, height=60)
        header.pack(fill=tk.X)
        tk.Label(header, text="Travel Assistant", fg="white", bg=self.HEADER_COLOR, 
                 font=("Segoe UI", 12, "bold"), pady=15).pack()

        # Chat Window
        self.chat_display = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, state='disabled', bg=self.BG_COLOR,
            font=("Segoe UI", 11), borderwidth=0, highlightthickness=0, pady=10
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)

        # Bubble Alignment Configurations
        # Right aligned for User
        self.chat_display.tag_configure("user", background=self.USER_BUBBLE, 
                                        lmargin1=100, lmargin2=100, rmargin=20, 
                                        spacing1=2, spacing3=2)
        
        self.chat_display.tag_configure("bot", background=self.BOT_BUBBLE, 
                                        lmargin1=20, lmargin2=20, rmargin=100, 
                                        spacing1=2, spacing3=2)
        
        self.chat_display.tag_configure("match", font=("Segoe UI", 9, "italic"), foreground="#555555")
        self.chat_display.tag_configure("meta", font=("Segoe UI", 8), foreground="gray")

        # Input Area
        input_frame = tk.Frame(self.root, bg="#F0F0F0", pady=10)
        input_frame.pack(fill=tk.X)
        
        self.user_input = tk.Entry(input_frame, font=("Segoe UI", 12), relief=tk.FLAT, bd=8)
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        self.user_input.bind("<Return>", lambda e: self.handle_send())

        send_btn = tk.Button(input_frame, text="SEND", command=self.handle_send, 
                             bg=self.HEADER_COLOR, fg="GREEN", font=("Segoe UI", 9, "bold"),
                             relief=tk.FLAT, padx=20, pady=5)
        send_btn.pack(side=tk.RIGHT, padx=10)

    def append_bubble(self, sender, message, matched_q=None, score=None):
        self.chat_display.config(state='normal')
        time = datetime.now().strftime("%H:%M")
        
        if sender == "You":
            # Removed the leading/trailing \n to tighten the bubble
            self.chat_display.insert(tk.END, f"{message}\n", "user")
            self.chat_display.insert(tk.END, f"{time} ✓✓\n", ("user", "meta"))
        else:
            # Removed extra \n between matched question and answer
            if matched_q:
                self.chat_display.insert(tk.END, f"MATCHED: \"{matched_q}\"\n", ("bot", "match"))
            
            self.chat_display.insert(tk.END, f"{message}\n", "bot")
            
            conf = f" (Confidence: {int(score*100)}%)" if score else ""
            self.chat_display.insert(tk.END, f"{time}{conf}\n", ("bot", "meta"))
        
        self.chat_display.config(state='disabled')
        self.chat_display.yview(tk.END)

    def handle_send(self):
        query = self.user_input.get().strip()
        if not query: return  # noqa: E701
        
        self.append_bubble("You", query)
        self.user_input.delete(0, tk.END)
        quest = self.tagger.process(query)

        if self.engine:
            ans, matched_s, score = self.engine.get_best_match(quest)
            # Add a tiny delay feel if you want, otherwise it's instant
            self.append_bubble("Bot", ans, matched_s, score)
         

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()

