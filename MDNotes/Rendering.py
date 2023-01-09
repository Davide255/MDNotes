import tkinter as tk
from tkhtmlview import HTMLScrolledText, RenderHTML

class RenderingWindow():

    root: tk.Tk = None 

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title = 'RENDERING WINDOW'
        self.root.geometry('200x400')
    
    def populate(self):
        html_label = HTMLScrolledText(self.root, html=RenderHTML('MDNotes\\tmp\\chunk.html'))
        html_label.pack(fill="both", expand=True)
        html_label.fit_height()

        return self

    def mainloop(self): self.root.mainloop()

    def destroy(self): self.root.destroy()