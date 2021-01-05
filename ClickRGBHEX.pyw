import win32api, win32gui
import colorsys
import time
import pyperclip
import ctypes
import tkinter as tk

# Multiple monitor fix
awareness = ctypes.c_int()
ctypes.windll.shcore.SetProcessDpiAwareness(2)

# Variable initializations
get=False
start=-1
running=True

# Functions
def turngeton():
    global get
    get=True
    btn_activate.config(state=tk.DISABLED, text="Waiting...")

def copyhex():
    global start
    start=time.process_time()
    btn_copyhex.config(state=tk.DISABLED, text="Copied!")
    pyperclip.copy(lbl_hexval["text"])

def close():
    global running
    running=False
    window.destroy()

# Window initializations
window = tk.Tk()
window.title("Click RGB/HEX")
window.attributes("-topmost", True)
window.resizable(False, False)
window.iconbitmap("icon.ico")

# Frame initializations
infoframe = tk.Frame(master=window)
infoframe.pack(fill=tk.BOTH, side=tk.LEFT)

colourframe = tk.Frame(master=window)
colourframe.pack(fill=tk.BOTH, side=tk.LEFT)

# Label initializations
lbl_rgb = tk.Label(master=infoframe, text="RGB value: ")
lbl_rgb.grid(row=0, column=0)

lbl_hex = tk.Label(master=infoframe, text="HEX value: ")
lbl_hex.grid(row=1, column=0)

lbl_rgbval = tk.Label(master=infoframe, text='', width=11, relief=tk.RIDGE)
lbl_rgbval.grid(row=0, column=1)

lbl_hexval = tk.Label(master=infoframe, text='', width=11, relief=tk.RIDGE)
lbl_hexval.grid(row=1, column=1)

lbl_name = tk.Label(master=infoframe, text="Ethan Maeda")
lbl_name.grid(row=2, column=1)

lbl_date = tk.Label(master=infoframe, text="Jan 2021")
lbl_date.grid(row=3, column=1)

lbl_preview = tk.Label(master=colourframe, text="Colour Preview", width=15)
lbl_preview.pack()

# Button initializations
btn_activate = tk.Button(master=infoframe, text="Activate", width=10, command=turngeton)
btn_activate.grid(row=2, column=0)

btn_copyhex = tk.Button(master=infoframe, text="Copy HEX", width=10, command=copyhex)
btn_copyhex.grid(row=3, column=0)

# Main program
while running:
    if get==True:
        if win32api.GetAsyncKeyState(0x01) < 0:
            x, y = win32gui.GetCursorPos()
            colour = win32gui.GetPixel(win32gui.GetDC(0), x, y)
            lbl_rgbval.config(text=', '.join(map(str, (colour & 255, (colour >> 8) & 255, (colour>>16) & 255))))
            lbl_hexval.config(text=("#%02x%02x%02x" % (colour & 255, (colour >> 8) & 255, (colour>>16) & 255)).upper())
            colourframe.config(bg=lbl_hexval["text"])
            btn_activate.config(state=tk.NORMAL, text="Activate")
            get=False
        
    if start!=-1 and start+1.5==time.process_time():
        btn_copyhex.config(state=tk.NORMAL, text="Copy HEX")
        start=-1

    window.protocol("WM_DELETE_WINDOW", close)  
    window.update()
