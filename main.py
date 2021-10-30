import tkinter as tk

def unmap(event):
    if event.widget is root:
        root.deiconify()
        
root = tk.Tk()

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

notchx = int(ws/9)
notchy = int(hs/40)

leftx = (ws/2) - (notchx/2)
rightx = (ws/2) + (notchx/2)

root.protocol('WM_DELETE_WINDOW', lambda: None)
root.geometry('%dx%d+%d+%d' % (notchx, notchy, leftx, 0))
root.overrideredirect(True)
root.configure(background='black')
root.attributes('-topmost',True)
root.bind('<Unmap>', unmap)

root.mainloop()
