import win32api, win32gui
import colorsys
import time
import pyperclip
import ctypes
import webbrowser
import tkinter as tk
from tkinter import font

# Multiple monitor fix
awareness = ctypes.c_int()
ctypes.windll.shcore.SetProcessDpiAwareness(2)

# Variable initializations
waiting = False
start = -1
running = True
url = "https://github.com/ethanmaeda/ClickRGBHEX"

howtostr = """How To Use
- Click \"Activate\" and upon your next
click, the program will retrieve the RGB
and HEX code of the pixel you clicked
- Click the \"Copy HEX\" button to copy
the HEX code to your clipboard"""

# Functions
def TurnGetOn():
    global waiting
    waiting = True
    btn_activate.config(state=tk.DISABLED, text="Waiting...")

def CopyHEX():
    global start
    start = time.process_time()
    btn_copyhex.config(state=tk.DISABLED, text="Copied!")
    pyperclip.copy(lbl_hexval["text"])

def OpenHowToUse():
    howtousewindow = tk.Toplevel(window, width=300, height=300)
    howtousewindow.title("How to Use")
    howtousewindow.attributes("-topmost", True)
    howtousewindow.resizable(False, False)
    howtousewindow.iconbitmap("icon.ico")
    lbl_howtouse = tk.Label(master=howtousewindow, justify=tk.LEFT, text=howtostr, font=default)
    lbl_howtouse.pack()

def OpenGitHub():
    webbrowser.open_new(url)

def Close():
    global running
    running = False
    window.destroy()

# Window initializations
window = tk.Tk()
window.title("Click RGB/HEX")
window.attributes("-topmost", True)
window.resizable(False, False)
window.iconbitmap("icon.ico")

# Font
default = font.Font(family="TkDefaultFont", size="12")

# Frame initializations
infoframe = tk.Frame(master=window, bd=4, relief=tk.GROOVE, padx=4, pady=4)
infoframe.pack(fill=tk.BOTH, side=tk.LEFT)

colourframe = tk.Frame(master=window, bd=4, relief=tk.GROOVE)
colourframe.pack(fill=tk.BOTH, side=tk.LEFT)

# Label initializations
lbl_rgb = tk.Label(master=infoframe, text="RGB value: ")
lbl_rgb.grid(row=0, column=0)

lbl_hex = tk.Label(master=infoframe, text="HEX value: ", pady=4)
lbl_hex.grid(row=1, column=0)

lbl_rgbval = tk.Label(master=infoframe, text='', width=11)
lbl_rgbval.grid(row=0, column=1)

lbl_hexval = tk.Label(master=infoframe, text='', width=11)
lbl_hexval.grid(row=1, column=1)

lbl_colourpreview = tk.Label(master=colourframe, text="Colour Preview", width=18)
lbl_colourpreview.pack()

# Button initializations
btn_activate = tk.Button(master=infoframe, text="Activate", width=10, command=TurnGetOn, relief=tk.GROOVE, bd=3)
btn_activate.grid(row=2, column=0)

btn_copyhex = tk.Button(master=infoframe, text="Copy HEX", width=10, command=CopyHEX, relief=tk.GROOVE, bd=3)
btn_copyhex.grid(row=3, column=0)

btn_howtouse = tk.Button(master=infoframe, text="How to Use", width=10, command=OpenHowToUse, relief=tk.GROOVE, bd=3)
btn_howtouse.grid(row=2, column=1)

btn_github = tk.Button(master=infoframe, text="GitHub", width=10, command=OpenGitHub, relief=tk.GROOVE, bd=3)
btn_github.grid(row=3, column=1)

# Main program
while running:
    if waiting:
        x, y = win32gui.GetCursorPos()
        colour = win32gui.GetPixel(win32gui.GetDC(0), x, y)
        rgb = (colour & 255, (colour >> 8) & 255, (colour>>16) & 255)
            
        colourframe.config(bg="#%02x%02x%02x" % rgb)
        lbl_colourpreview.config(bg="#%02x%02x%02x" % rgb, fg="#%02x%02x%02x" % (255-rgb[0], 255-rgb[1], 255-rgb[2]))
        
        if win32api.GetAsyncKeyState(0x01) < 0:
            lbl_rgbval.config(text=', '.join(map(str, rgb)))
            lbl_hexval.config(text=("#%02x%02x%02x" % rgb).upper())
            btn_activate.config(state=tk.NORMAL, text="Activate")
            waiting=False
        
    if start!=-1 and start+1.5==time.process_time():
        btn_copyhex.config(state=tk.NORMAL, text="Copy HEX")
        start=-1

    window.protocol("WM_DELETE_WINDOW", Close)  
    window.update()
