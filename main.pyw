from GUI import Application
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Transmitter")
    root.geometry("350x350")
    app = Application(master=root)
    app.mainloop()
