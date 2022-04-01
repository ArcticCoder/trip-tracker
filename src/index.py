import tkinter as tk
from ui.ui import UI

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Trip tracker")

    ui = UI(window)
    ui.start()

    window.mainloop()
