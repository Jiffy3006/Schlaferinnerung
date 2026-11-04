import tkinter as tk
from tkinter import ttk
import datetime

# --- EINSTELLUNGEN ---
ZIEL_STUNDE = 22
ZIEL_MINUTE = 0

class SchlafErinnerungApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Schlafenszeit!")
        self.root.geometry("400x250")
        self.root.resizable(False, False)
        
        # Fenster im Vordergrund halten
        self.root.attributes("-topmost", True)
        
        # UI-Elemente: Titel
        lbl_titel = tk.Label(
            root, 
            text="🌙 Zeit fürs Bett!", 
            font=("Helvetica", 18, "bold"), 
            fg="#2c3e50"
        )
        lbl_titel.pack(pady=15)

        # UI-Elemente: Text
        lbl_text = tk.Label(
            root, 
            text=f"Es ist {ZIEL_STUNDE:02d}:{ZIEL_MINUTE:02d} Uhr. Leg das Gerät weg und erhole dich!", 
            font=("Helvetica", 11),
            wraplength=350
        )
        lbl_text.pack(pady=10)

        # Snooze Frame
        frame_snooze = tk.Frame(root)
        frame_snooze.pack(pady=15)

        tk.Label(frame_snooze, text="Schlummern für:").pack(side=tk.LEFT, padx=5)
        
        self.snooze_zeit = tk.IntVar(value=10)
        snooze_dropdown = ttk.Combobox(
            frame_snooze, 
            textvariable=self.snooze_zeit, 
            values=[5, 10, 15, 30], 
            width=5, 
            state="readonly"
        )
        snooze_dropdown.pack(side=tk.LEFT, padx=5)
        tk.Label(frame_snooze, text="Minuten").pack(side=tk.LEFT)

        # Buttons
        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=10)

        btn_snooze = tk.Button(
            frame_buttons, 
            text="😴 Snooze", 
            command=self.snooze, 
            bg="#f39c12", 
            fg="white", 
            font=("Helvetica", 10, "bold"),
            width=12
        )
        btn_snooze.pack(side=tk.LEFT, padx=10)

        btn_gute_nacht = tk.Button(
            frame_buttons, 
            text="Gute Nacht!", 
            command=self.gute_nacht, 
            bg="#27ae60", 
            fg="white", 
            font=("Helvetica", 10, "bold"),
            width=12
        )
        btn_gute_nacht.pack(side=tk.LEFT, padx=10)

        # WICHTIG: Das Fenster beim Start direkt unsichtbar in den Hintergrund schicken!
        self.root.withdraw()
        
        # Uhrzeit-Prüfung starten
        self.pruefe_uhrzeit()

    def zeige_popup(self):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def snooze(self):
        minuten = self.snooze_zeit.get()
        self.root.withdraw()
        # Nach X Minuten erneut aufrufen (in Millisekunden)
        self.root.after(minuten * 60 * 1000, self.zeige_popup)

    def gute_nacht(self):
        self.root.withdraw()
        # Wartet 20 Stunden, bis es am nächsten Tag wieder prüft
        self.root.after(20 * 3600 * 1000, self.pruefe_uhrzeit)

    def pruefe_uhrzeit(self):
        jetzt = datetime.datetime.now()
        
        # Prüft, ob es exakt 22:00 Uhr ist
        if jetzt.hour == ZIEL_STUNDE and jetzt.minute == ZIEL_MINUTE:
            self.zeige_popup()
            # 61 Sekunden warten, damit das Popup in dieser Minute nicht mehrfach triggert
            self.root.after(61000, self.pruefe_uhrzeit)
        else:
            # Alle 30 Sekunden im Hintergrund die Uhrzeit überprüfen
            self.root.after(30000, self.pruefe_uhrzeit)

if __name__ == "__main__":
    root = tk.Tk()
    app = SchlafErinnerungApp(root)
    root.mainloop()