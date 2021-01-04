import win32api, win32gui
import pyautogui
import colorsys
import time
import pyperclip
import tkinter as tk

# Variable initializations
rgbstr=""
hexstr=""
get=False
copied=False
start=-1
running=True

# Functions
def turngeton():
    global get
    get=True

def copyhex():
    pyperclip.copy(hexstr)
    global copied
    copied=True

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

lbl_rgbval = tk.Label(master=infoframe, text=rgbstr, width=11, relief=tk.RIDGE)
lbl_rgbval.grid(row=0, column=1)

lbl_hexval = tk.Label(master=infoframe, text=hexstr, width=11, relief=tk.RIDGE)
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
        btn_activate.config(state=tk.DISABLED, text="Waiting...")
        
        if win32api.GetAsyncKeyState(0x01) < 0:
            x, y = pyautogui.position()
            colour = win32gui.GetPixel(win32gui.GetDC(None), x, y)
            rgb=(colour & 255, (colour >> 8) & 255, (colour>>16) & 255)

            rgbstr = ', '.join(map(str, rgb))
            hexstr = "#%02x%02x%02x" % rgb
            hexstr=hexstr.upper()
            get=False
    else:
        btn_activate.config(state=tk.NORMAL, text="Activate")
        
    if copied==True:
        start=time.process_time()
        btn_copyhex.config(state=tk.DISABLED, text="Copied!")
        copied=False

    if copied==False and start+1.5==time.process_time():
        btn_copyhex.config(state=tk.NORMAL, text="Copy HEX")
    
    lbl_rgbval.config(text=rgbstr)
    lbl_hexval.config(text=hexstr)
    
    if hexstr!="":
        colourframe.config(bg=hexstr)

    window.protocol("WM_DELETE_WINDOW", close)  
    window.update()
