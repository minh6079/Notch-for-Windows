import tkinter as tk

root = tk.Tk()

def unmap(event):
    if event.widget is root:
        root.deiconify()
        

def screen_stuff():
    
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()

    notchx = int(ws/9)
    notchy = int(hs/30)

    leftx = (ws/2) - (notchx/2)
    rightx = (ws/2) + (notchx/2)

    root.geometry('%dx%d+%d+%d' % (notchx, notchy, leftx, 0))

screen_stuff()

root.configure(background='black')

root.protocol('WM_DELETE_WINDOW', lambda: None)
root.overrideredirect(True)
root.attributes('-topmost',True)
root.bind('<Unmap>', unmap)

root.mainloop()
